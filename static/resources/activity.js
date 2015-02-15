angular.module('FriskisApp').factory('Activity', function($resource) {
    return $resource('/activities');
});
