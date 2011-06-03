$(document).ready(function() {
    $.rcall('vendor.mymod1', 'myfunc1', {arg1: 1, arg2: 2}, function(data) {
        $('#results').append('arg1: ' + data.args[0] + ' arg2: ' + data.args[0] + '<br>');
    });

    $.rcall('vendor.mymod1', 'myfunc2', {name: 'Me'}, function(data) {
        $('#results').append(data.r + '<br>');
    });

    $.rcall('vendor.mymod1', 'myfunc3', {}, function(data) {
        $('#results').append(data.r + '<br>');
    });

    $.rcall('vendor.mymod1', 'myfunc4', {_args: ['hash me']}, function(data) {
        $('#results').append(data.r + '<br>');
    });
});
