'use strict';

angular.module('FriskisApp').controller('ActivityListViewController', function ($scope, $http, $mdBottomSheet, Activity) {
    var activitiesByDate = {};

    function getDateKey(date) {
        return moment(date).format('YYYY-MM-DD')
    }

    function createDateSequence(length) {
        var date = moment();
        var result = []

        for (var i = 0; i < length; i++) {
            result.push(date.clone().toDate());
            date.add(1, 'days');
        };

        return result;
    }

    $scope.dates = createDateSequence(5);
    console.log($scope.dates);

    $http.get('/activities').then(function (response) {
        response.data.result.forEach(function (activity) {
            activity.start = new Date(activity.start_dt);
            activity.end = new Date(activity.end_dt);

            var key = getDateKey(activity.start_dt);

            if (!activitiesByDate[key]) {
                activitiesByDate[key] = [];
            }
            activitiesByDate[key].push(activity);
        });
        $scope.activitiesByDate = activitiesByDate;
    })

    $scope.getActivities = function (date) {
        return $scope.activitiesByDate[getDateKey(date)];
    }


}).controller('ActivitySheetController', function($scope, $mdBottomSheet, activity) {
    $scope.activity = activity;

    $scope.listItemClick = function() {
        $mdBottomSheet.hide(clickedItem);
    };
});
