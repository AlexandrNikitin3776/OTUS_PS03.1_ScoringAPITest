#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from scoringapi import api


class TestField:
    @pytest.mark.parametrize('value, required, nullable', [
        (0, True, True),
        ('', True, True),
        ([], True, True),
        (None, False, True),
        ((0, '0'), False, False),
    ])
    def test_valid_Field(self, value, required, nullable):
        field = api.Field(required=required, nullable=nullable)
        field.value = value
        assert field.isvalid()

    @pytest.mark.parametrize('value, required, nullable, exc', [
        (None, True, True, ValueError),
        ('', False, False, ValueError),
        ([], False, False, ValueError),
    ])
    def test_invalid_Field(self, value, required, nullable, exc):
        field = api.Field(required=required, nullable=nullable)
        field.value = value
        with pytest.raises(exc):
            field.isvalid()


class TestCharField:
    @pytest.mark.parametrize('value', [
        '0',
        'info@example.com',
    ])
    def test_valid_CharField(self, value):
        field = api.CharField(required=False, nullable=True)
        field.value = value
        assert field.isvalid()

    @pytest.mark.parametrize('value, exc', [
        (131131, TypeError),
        (('h&f',), TypeError),
        ({'h&f': 123}, TypeError),
    ])
    def test__invalid_CharField(self, value, exc):
        field = api.CharField(required=False, nullable=True)
        field.value = value
        with pytest.raises(exc):
            field.isvalid()


class TestEmailField:
    # string, has @, optional, can be empty
    @pytest.mark.parametrize('value', [
        'info@example.com',
        '@',
        '!!!@@@###$%%^',
    ])
    def test_valid_EmailField(self, value):
        field = api.EmailField(required=False, nullable=True)
        field.value = value
        assert field.isvalid()

    @pytest.mark.parametrize('value, exc', [
        ('11111111', ValueError),
        ('0', ValueError),
        (131131, TypeError),
        (('h&f',), TypeError),
        ({'h&f': 123}, TypeError),
    ])
    def test__invalid_EmailField(self, value, exc):
        field = api.EmailField(required=False, nullable=True)
        field.value = value
        with pytest.raises(exc):
            field.isvalid()


class TestPhoneField:
    # string or number, 11 symbols length, starts with 7, optional, can be empty
    @pytest.mark.parametrize('value', [
        70123456789,
        '70123456789',
    ])
    def test_valid_PhoneField(self, value):
        field = api.PhoneField(required=False, nullable=True)
        field.value = value
        assert field.isvalid()

    @pytest.mark.parametrize('value, exc', [
        (80123456789, ValueError),
        (7, ValueError),
        ('80123456789', ValueError),
        ('7----------', ValueError),
        ('0', ValueError),
        (('h&f',), TypeError),
        ({'h&f': 123}, TypeError),
    ])
    def test__invalid_PhoneField(self, value, exc):
        field = api.PhoneField(required=False, nullable=True)
        field.value = value
        with pytest.raises(exc):
            field.isvalid()


class TestDateField:
    # date in DD.MM.YYYY format, optional, can be empty
    @pytest.mark.parametrize('value', [
        '01.01.0001',
        '17.10.1917',
        '13.06.2020',
    ])
    def test_valid_DateField(self, value):
        field = api.DateField(required=False, nullable=True)
        field.value = value
        assert field.isvalid()

    @pytest.mark.parametrize('value, exc', [
        ('1.1.1', ValueError),
        ('01.01.0000', ValueError),
        ('1.10.2019', ValueError),
        (('h&f',), TypeError),
        ({'h&f': 123}, TypeError),
    ])
    def test__invalid_DateField(self, value, exc):
        field = api.DateField(required=False, nullable=True)
        field.value = value
        with pytest.raises(exc):
            field.isvalid()


class TestBirthDayField:
    # date in DD.MM.YYYY format, age isn't more than 70 years, optional, can be empty
    @pytest.mark.parametrize('value', [
        '17.10.1967',
        '13.05.2020',
    ])
    def test_valid_BirthDayField(self, value):
        field = api.BirthDayField(required=False, nullable=True)
        field.value = value
        assert field.isvalid()

    @pytest.mark.parametrize('value, exc', [
        ('01.01.1950', ValueError),
        ('17.10.2917', ValueError),
        ('1.1.1', ValueError),
        ('01.01.0000', ValueError),
        ('1.10.2019', ValueError),
        (('h&f',), TypeError),
        ({'h&f': 123}, TypeError),
    ])
    def test__invalid_BirthDayField(self, value, exc):
        field = api.BirthDayField(required=False, nullable=True)
        field.value = value
        with pytest.raises(exc):
            field.isvalid()


class TestGenderField:
    # number 0, 1 or 2, optional, can be empty
    @pytest.mark.parametrize('value', [
        0,
        1,
        2,
    ])
    def test_valid_GenderField(self, value):
        field = api.GenderField(required=False, nullable=True)
        field.value = value
        assert field.isvalid()

    @pytest.mark.parametrize('value, exc', [
        (4, ValueError),
        (-1, ValueError),
        ('1.1.1', TypeError),
        (('h&f',), TypeError),
        ({'h&f': 123}, TypeError),
    ])
    def test_invalid_GenderField(self, value, exc):
        field = api.GenderField(required=False, nullable=True)
        field.value = value
        with pytest.raises(exc):
            field.isvalid()


class TestClientIDsField:
    # array of numbers, required, not empty
    @pytest.mark.parametrize('value', [
        [0, ],
        [1, 1],
    ])
    def test_valid_ClientIDsField(self, value):
        field = api.ClientIDsField(required=True, nullable=False)
        field.value = value
        assert field.isvalid()

    @pytest.mark.parametrize('value, exc', [
        ([], ValueError),
        (['1', '2', '3', '4'], TypeError),
        (-1, TypeError),
        ('1.1.1', TypeError),
        (('h&f',), TypeError),
        ({'h&f': 123}, TypeError),
    ])
    def test_invalid_ClientIDsField(self, value, exc):
        field = api.ClientIDsField(required=True, nullable=False)
        field.value = value
        with pytest.raises(exc):
            field.isvalid()


class TestArgumentsField:
    # dictionary (object in json terminology), required, can be empty
    @pytest.mark.parametrize('value', [
        {'a': [0, ]},
        {},
    ])
    def test_valid_ArgumentsField(self, value):
        field = api.ArgumentsField(required=True, nullable=True)
        field.value = value
        assert field.isvalid()

    @pytest.mark.parametrize('value, exc', [
        (['1', '2', '3', '4'], TypeError),
        (-1, TypeError),
        ('1.1.1', TypeError),
        (('h&f',), TypeError),
    ])
    def test_invalid_ArgumentsField(self, value, exc):
        field = api.ArgumentsField(required=True, nullable=True)
        field.value = value
        with pytest.raises(exc):
            field.isvalid()
