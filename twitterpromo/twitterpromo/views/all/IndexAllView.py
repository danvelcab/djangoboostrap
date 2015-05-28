import httplib
from urllib import urlencode
import urllib2
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.views.generic import View
from pip._vendor.requests.packages.urllib3.util import url

from twitterpromo.twitter.ioauth import parse_host, parse_port, parse_path, Consumer, token_from_string


__author__ = 'Daniel'


class IndexAllView(View):
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    request_token = None

    @staticmethod
    def index(request):
        consumer_key = 'v7fLFwr4uuoaNeCfUW2a8L8JT'
        consumer_secret = 'noDZz5apvNK5sgfClH6xVXYqCcloFZHJVREiKGtQt7LhssMinK'
        consumer = Consumer(consumer_key, consumer_secret)
        # params = {'oauth_callback': "https://api.twitter.com/oauth/request_token"}
        # params = {'oauth_callback': 'localhost'}
        # params = {'oauth_callback': 'http%3A%2F%2Flocalhost%2Fsign-in-with-twitter%2F'}
        params = {}
        signature = consumer.sign_request('https://api.twitter.com/oauth/request_token', 'POST', params)
        headers = {'Authorization': signature.get_header()}
        conn = httplib.HTTPSConnection(
            parse_host('https://api.twitter.com/oauth/request_token'),
            parse_port('https://api.twitter.com/oauth/request_token'))
        conn.request('POST', parse_path('https://api.twitter.com/oauth/request_token'), '', headers)
        response = conn.getresponse()

        body = response.read()

        IndexAllView.request_token = token_from_string(body)

        conn.close()

        return redirect('https://api.twitter.com/oauth/authorize?oauth_token=' + str(IndexAllView.request_token.key))

    @staticmethod
    def twitter_callback(request):
        conn = httplib.HTTPSConnection(
            parse_host('https://api.twitter.com/'),
            parse_port('https://api.twitter.com/'))
        consumer_key = 'v7fLFwr4uuoaNeCfUW2a8L8JT'
        consumer_secret = 'noDZz5apvNK5sgfClH6xVXYqCcloFZHJVREiKGtQt7LhssMinK'
        request_token = IndexAllView.request_token
        consumer = Consumer(consumer_key, consumer_secret, request_token)
        params = {'oauth_verifier': str(request.REQUEST['oauth_verifier'])}
        signature = consumer.sign_request('https://api.twitter.com/oauth/access_token', 'POST', params)
        headers = {'Authorization': signature.get_header()}
        conn.request('POST', parse_path('https://api.twitter.com/oauth/access_token'), urlencode(params), headers)
        response = conn.getresponse()
        body = response.read()
        access_token = token_from_string(body)
        conn.close()

        consumer = Consumer(consumer_key, consumer_secret, access_token)
        # params = {'text': 'hola', 'user_id' : '2706244140', 'screen_name': 'GadesGamesPromo'}
        # signature = consumer.sign_request('https://api.twitter.com/1.1/direct_messages/new.json', 'POST', params)

        conn = httplib.HTTPSConnection(
            parse_host('https://api.twitter.com/1.1/friends/ids.json'),
            parse_port('https://api.twitter.com/1.1/friends/ids.json'))

        params = {'user_id': "2706244140" , 'screen_name': 'GadesGamesPromo'}
        # params = {'cursor': '-1', 'screen_name' : 'twitterapi', 'count' : '5000'}
        # signature = consumer.sign_request('https://api.twitter.com/1.1/friends/ids.json', params)
        signature = consumer.sign_request('https://api.twitter.com/1.1/friends/ids.json?user_id=2706244140','','')

        headers = {'Authorization': signature.get_header()}
        conn.request('GET', parse_path('https://api.twitter.com/1.1/friends/ids.json')+'%3Fuser_id%253D2706244140',urlencode(''), headers)
        # conn.request('POST', parse_path('https://api.twitter.com/1.1/direct_messages/new.json'), urlencode(params),
        #              headers)

        response = conn.getresponse()
        body = response.read()
        conn.close()
        return HttpResponse(response)




