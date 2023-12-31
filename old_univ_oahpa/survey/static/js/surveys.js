/* jshint strict: false */
/* jshint camelcase: false */

function listContainsObject(_list, _obj, field) {
    for (var i = 0; i < _list.length; i++) {
        if(_list[i][field] === _obj[field]) {
            return i;
        }
    }
    return -1;
}

var Surveys = angular.module('Surveys', ['ngCookies', 'angular-loading-bar']).
    config(function($interpolateProvider, $httpProvider) {
        // set template expression symbols
        $interpolateProvider.startSymbol('<%');
        $interpolateProvider.endSymbol('%>');
        $httpProvider.defaults.withCredentials = true;
    });

function SurveyClient($scope, $http, $element, $cookies) {
    'use strict';

    var survey_source = $element.attr('ng-source') + 'surveys/' ;
    var answer_target = $element.attr('ng-source') + 'answer/' ;
    $scope.survey_answers = {};
    $scope.form_success = false;
    $scope.next_survey_button = false;

    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

    //  GET output, serialize to POST
    //
    //  {
    //      "survey": 1, 
    //      "user_answers": [
    //          {
    //              "question": 1, 
    //              "answer_text": "plah plah"
    //          }, 
    //          {
    //              "question": 3, 
    //              "answer_text": "plah plah"
    //          }
    //      ]
    //  }

    function formatAnswers(answers) {
        var _answers = [];
        var k ;

        for (k in answers) {
            _answers.push({
                'question': parseInt(k),
                'answer_text': answers[k],
            });
        }

        return _answers;
    }

    $scope.submitForm = function($event) {
        var config = {
            withCredentials: true,
        };

        var post_data = [];
        var key;

        for (key in $scope.survey_answers) {
            var survey_input = $scope.survey_answers[key];

            var post_survey = {};
            post_survey.survey = key;
            post_survey.user_answers = formatAnswers(survey_input);

            post_data.push(post_survey);
        }

        $http.post(answer_target, post_data[0], config)
         .success( function(data) {
            $scope.form_success = true;
            $scope.response = true;
            $scope.response = data;
            $scope.results = data;
            if (data.errors) {
                $scope.form_error = data.non_field_errors;
                $scope.validation_errors = data;
                // other errors go here.
                $scope.success = false;
            } 
        }).error( function(data, status, headers, config) {
            $scope.response = true;
            var permitted = [
                400,
            ];

            if (permitted.indexOf(status) > -1) {
                $scope.form_error = data.non_field_errors.join(' ');
            } else {
                $scope.form_error = "Server or connection error: " + status + ".";
            }
        });
    };

    // Push the Tasks that the user has access to into the not in use box.
    $http.get(survey_source).success(function(data){
        $scope.survey = false;
        if (data.results.length > 0) {
            $scope.survey = data.results[0];
        }
        if (data.results.length > 1) {
            $scope.next_survey_button = true;
        }
        $scope.survey_answers = {};
        if ($scope.survey) {
            $scope.survey_answers[$scope.survey.id] = {};
        }
    })
}
