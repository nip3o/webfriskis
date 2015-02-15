'use strict';

angular.module('FriskisApp').controller('ActivityListViewController', function ($scope, $http, $mdBottomSheet, Activity) {
    $scope.dates = [new Date(2015, 1, 15), new Date(2015, 1, 16), new Date(2015, 1, 17), new Date(2015, 1, 18)];

    $http.get('/activities').then(function (response) {
        $scope.activities = response.data.result;
        console.log($scope.activities);
    })

    // Activity.query(function (activities) {
    //     $scope.activities = activities;
    // });


}).controller('ActivitySheetController', function($scope, $mdBottomSheet, activity) {
    $scope.activity = activity;

    $scope.listItemClick = function() {
        $mdBottomSheet.hide(clickedItem);
    };
});
