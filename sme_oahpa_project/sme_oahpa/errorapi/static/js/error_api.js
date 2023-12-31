﻿/* jshint strict: false */
/* jshint camelcase: false */

var ErrorAPI = angular.module('ErrorAPI', ['ngCookies', 'angular-loading-bar']).
    config(function($interpolateProvider, $httpProvider) {
        // set template expression symbols
        $interpolateProvider.startSymbol('<%');
        $interpolateProvider.endSymbol('%>');
        $httpProvider.defaults.withCredentials = true;
    });

ErrorAPI.controller('ErrorRequester', function($scope, $http, $element, $cookies) {

    function handle_api_response (data) {

        $scope.response = data;

        if(data.messages.length > 0) {
            $scope.messages = data.messages;
            $scope.analyzer = data.fst[0];
            $scope.no_errors = false;
        } else {
            $scope.messages = false;
            $scope.analyzer = false
            $scope.no_errors = true;
        }

    }

    var feedback_url = $element.attr('data-lookup-url') ;

    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

    if ($element.attr('data-error-watch')) {
        var css_selector = $element.attr('data-error-watch');
    } else {
        var css_selector = "a[data-error-fst]";
    }

    $element.find("form").bind('submit', function ($event) {

        var feedback_data = {
            'lookup': $scope.text_input,
        }
        $scope.no_errors = false;

        if ($scope.task) {
            feedback_data['task'] = $scope.task;
        }

        if ($scope.lemma) {
            feedback_data['intended_lemma'] = $scope.lemma;
        }

        var config = {
            withCredentials: true,
            headers: { 'Content-Type': 'application/json' }
        };

        feedback_data = JSON.stringify(feedback_data);

        $http.post(feedback_url, feedback_data, config)
             .success(handle_api_response);
        
    });

    $element.find(css_selector).bind('click', function ($event) {

        $event.preventDefault();

        var feedback_link = $($event.target);

        function handle_api_feedback_popover (data) {
            handle_api_response(data);

            if (window.last_feedback) {
                last_feedback.popover('destroy');
            }

            if ($scope.messages) {

                // Collect feedback messages.
                // Attempted to do this by injecting an angular template, but
                // it was too tricky.
                var message_body_snippet = "<ul class='errorapi_messages'>";

                for (_i = 0, _len = $scope.messages.length; _i < _len; _i++) {
                    msg = $scope.messages[_i];
                    console.log(msg);

                    for (_j = 0, _lenz = msg.message.length; _j < _lenz; _j++) {
                        m = msg.message[_j];
                        message_body_snippet += "<li>" ;
                        if (m.title) {
                            message_body_snippet += m.title + ": " + m.description;
                        }
                        if (m.article) {
                            message_body_snippet += "<br /><a href='" + m.article + ">Klikk for å lese mer</a>";
                        }
                        message_body_snippet += "</li>" ;
                    }

                }
                message_body_snippet += "</ul>";

            } else {
                // TODO: localize
                message_body_snippet = "<p>No errors :)</p>";
            }

            var _wrapped_template = '<div class="bootstrap-styles"><div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div></div>';
            feedback_link.popover({
                template: _wrapped_template,
                title: 'Feedback',
                content: message_body_snippet,
                html: true,
                trigger: 'hover focus',
            });

            feedback_link.popover('show');
            window.last_feedback = feedback_link;
        }

        // Prepare request
        var form  = $(feedback_link).attr('data-input-form') || $(feedback_link).html();
        var task  = $(feedback_link).attr('data-task');
        var lemma = $(feedback_link).attr('data-lemma');

        // JSON? 
        var feedback_data = {
            'lookup': form,
        }

        if (task) {
            feedback_data['task'] = task;
        }

        if (lemma) {
            feedback_data['intended_lemma'] = lemma;
        }

        var config = {
            withCredentials: true,
            headers: { 'Content-Type': 'application/json' }
        };

        feedback_data = JSON.stringify(feedback_data);

        $http.post(feedback_url, feedback_data, config)
             .success(handle_api_feedback_popover);

    }); // click event

});
