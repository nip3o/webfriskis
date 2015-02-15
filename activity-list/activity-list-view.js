'use strict';

angular.module('FriskisApp').controller('ActivityListViewController', function ($scope, $mdBottomSheet) {
    $scope.dates = [new Date(2015, 1, 15), new Date(2015, 1, 16), new Date(2015, 1, 17), new Date(2015, 1, 18)];

    var activities = [
        {
            name: 'Gym öppet',
            date: new Date(),
            placesLeft: 2,
            placesTotal: 30,
            time: '14:30 - 20:00',
            location: 'Kanonhuset',
            leader: '',
        }, {
            name: 'Power Hour',
            date: new Date(),
            placesLeft: 2,
            placesTotal: 30,
            time: '16:00 - 17:00',
            location: 'Kanonhuset',
            leader: 'Madeleine Söderstedt Sjöberg',
        }, {
            name: 'Jympa medel',
            date: new Date(),
            placesLeft: 2,
            placesTotal: 30,
            time: '16:45 - 17:45',
            location: 'Kanonhuset',
            leader: 'Anna Wretman',
        },
    ];

    $scope.activitiesForDate = function (date) {
        console.log(date);
        return activities;
    }

}).controller('ActivitySheetController', function($scope, $mdBottomSheet, activity) {
    $scope.activity = activity;

    $scope.listItemClick = function() {
        $mdBottomSheet.hide(clickedItem);
    };
});
