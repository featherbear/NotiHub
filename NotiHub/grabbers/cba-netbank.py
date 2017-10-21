# -*- coding: utf-8 -*-
"""
NotiHub
Copyright 2017 Andrew Wong <featherbear@navhaxs.au.eu.org>

The following code is licensed under the MIT License
"""

__VERSION__ = "0.0.1"

import mechanicalsoup
from __stub__ import Grabber


class grabber(Grabber):
    baseUrl = "https://www.my.commbank.com.au/"
    loginUrl = "netbank/Logon/Logon.aspx"

    def __init__(self):
        self.browser = mechanicalsoup.StatefulBrowser()
        self.browser.open(self.baseUrl + self.loginUrl)
        self.browser.select_form("#form1")
        self.browser['txtMyClientNumber$field'] = ""
        self.browser['txtMyPassword$field'] = ""
        self.browser['JS'] = 'E'
        response = self.browser.submit_selected()
        page = self.browser.get_current_page()
        assert page.find("title").text.strip() == "NetBank - Home"

        self.accounts = []
        for account_row in page.select(".main_group_account_row"):
            nickname = account_row.select(".NicknameField a")[0].text
            bsb = account_row.select(".BSBField .field")[0].text
            account_number = account_row.select(".AccountNumberField .field")[0].text
            try:
                balance = account_row.select("td.AccountBalanceField span.Currency")[0].text
            except IndexError:
                balance = 0
            try:
                available = account_row.select("td.AvailableFundsField span.Currency")[0].text
            except IndexError:
                available = 0

            self.accounts.append({
                # "url": nickname.get('href'),
                "nickname": nickname,
                "bsb": bsb,
                "account_number": account_number,
                "balance": balance,
                "available": available
            })

    def grab(self, search=None):
        return list(filter(
            lambda a: any(map(lambda b: search.lower().replace(" ", "") in b.lower().replace(" ", ""), a.values())),
            self.accounts)) if search else self.accounts
