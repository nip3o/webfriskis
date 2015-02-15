angular.module('FriskisApp').directive('activityList', function ($mdBottomSheet) {
    return {
        restrict: 'E',
        templateUrl: '/static/activity-list/activity-list.html',
        scope: {
            items: '=',
        },
        link: function (scope, element, attrs) {
            scope.select = function ($event, activity) {
                $mdBottomSheet.show({
                    templateUrl: '/static/activity-list/activity-sheet.html',
                    controller: 'ActivitySheetController',
                    targetEvent: $event,
                    locals: {
                        activity: activity,
                    },
                }).then(function(clickedItem) {

                });
            };
        }
    };
});
