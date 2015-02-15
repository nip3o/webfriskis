angular.module('FriskisApp', ['ngMaterial', 'ngResource']).config(function($mdThemingProvider) {
    $mdThemingProvider.theme('default')
        .primaryPalette('red')
        .accentPalette('blue');
});
