#!/usr/bin/python

from boto import sys as botosys
from boto import s3 as botos3

import requests
import getpass
import ConfigParser
import base64
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup 
from os.path import expanduser 
from urlparse import urlparse, urlunparse 
from requests_ntlm import HttpNtlmAuth


class SessionObtainer():

	

	def __init__(self):
		self.username = ""
		self.password = ""
		self.AWS_CONFIG_FILE = '/.aws/credentials'
		self.sslverification = True 			#Please keep on True
		# Write the AWS STS token into the AWS credential file
		home = expanduser("~")
		filename = home + self.AWS_CONFIG_FILE
		# Read in the existing config file
		config = ConfigParser.RawConfigParser()
		config.read(filename)

		self.idpentryurl = config.get("default", "saml_endpoint")

	def gather_IdP_response(self):
		print "Username:",
		self.username = raw_input()
		self.password = getpass.getpass()
		print ''

		# Initiate session handler 
		self.session = requests.Session() 
		 
		# Programatically get the SAML assertion 
		# Set up the NTLM authentication handler by using the provided credential 
		self.session.auth = HttpNtlmAuth(self.username, self.password, self.session) 
		 
		# Opens the initial AD FS URL and follows all of the HTTP302 redirects 
		self.response = self.session.get(self.idpentryurl, verify=self.sslverification) 
		 
		# Debug the response if needed 
		print (response.text)

		# Overwrite and delete the credential variables, just for safety
		username = '##############################################'
		password = '##############################################'
		del username
		del password

	def check_session(self):
		home = expanduser("~")
		filename = home + self.AWS_CONFIG_FILE
		config = ConfigParser.RawConfigParser()
		config.read(filename)

		if config.has_section('saml'):
			return True
		else:
			return False

class SessionNotStoredException(Exception):
	msg = "User is not authenticated"