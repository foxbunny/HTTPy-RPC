//
// HTTPy-RPC
//
// Copyright (c)2011, by Branko Vukelic <branko@herdhound.com>
// Herd Hound http://www.herdhound.com/
//
// v0.1
//

(function($) {

    function RPCError(msg) { this.msg = msg; }
    RPCError.prototype.toString = function() { return 'RPCError: ' + this.msg; };

    $.rrequest = function(mod, func, args, callback, useJSONP) {
        var respType = useJSONP ? 'jsonp' : 'json';
        var url = "/rpc/" + mod + "/" + func;
        
        callback = callback || function(data) {
            $(document).trigger('rpcComplete', 
                {module: mod, func: func, args: args, data: data});
        };

        $.ajax({
            url: url,
            type: 'POST',
            data: args,
            dataType: respType,
            success: function(response, status, XHRObj) {
                callback(response);
            },
            error: function(XHRObj, status, error) {
                var errorMessage;
                if (XHRObj.status === 400) {
                    errorMessage = XHRObj.responseText;
                    throw RPCError(errorMessage);
                } else {
                    throw RPCError('Unknown error');
                }
            }
        });
    };

    $.rcall = function(mod, func, args, callback, useJSONP) {
        $(document).bind('rpcComplete', function(response) {
            if (response.module === mod && response.func === func && response.args === args) {
                return response.data;
            }
        });
        $.rrequest(mod, func, args, callback, useJSONP);
    };

}(jQuery));
