# -*- coding: utf-8 -*-

class Handler(object):
    def __init__(self,caller,method,args = []):
        #args: [1,2,3]
        self.caller = caller
        self.method = method
        self.args = args

    def run(self):
        if self.caller and self.method:
            self.method(* self.args)