var app = angular.module("share.app.resource", ['share.api']);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});


/*
app.controller("AppController", function($scope, $http){
    $scope.posts = [
        {
            "author": "Joe",
            "title" : "Sample post 1",
            "body" : "This is a body"
        },
         {
            "author": "Dave",
            "title" : "Sample post 2",
            "body" : "This is another body"
        }

    ]
});
*/

//var app = angular.module('example.app.resource', ['example.api']);
/*
app.controller('AppController', [
  '$scope', 'Share', function($scope, Share) {
     $scope.posts = Share.query();
     //$scope.tags = ShareTag.query();
  }
]);
/*
app.controller('AppController', [
  '$scope', 'Share', 'ShareTag', function($scope, Share, ShareTag) {
    $scope.shares = {};
    $scope.posts = Share.query();
    return $scope.posts.$promise.then(function(results) {
      return angular.forEach(results, function(post) {
        return $scope.tags[post.id] = ShareTag.query({
          share_id: post.id
        });
      });
    });
  }
]);
*/

app.controller('AppController', [
  '$scope', 'Share', 'ShareLink', function($scope, Share, ShareLink) {
   // $scope.tags = {};
    $scope.links = {};
    $scope.posts = Share.query();


    return $scope.posts.$promise.then(function(results) {
      return angular.forEach(results, function(post) {
        return $scope.links[post.id] = ShareLink.query({
          share_id: post.id
        });
      });
    });


           /* return $scope.posts.$promise.then(function(results) {
      return angular.forEach(results, function(post) {
        return $scope.tags[post.id] = ShareTag.query({
          share_id: post.id
        });
      });
    });
     return $scope.posts.$promise.then(function(results) {
      return angular.forEach(results, function(post) {
        return $scope.links[post.id] = ShareLink.query({
          share_id: post.id
        });
      });



    });*/

  }
]);

/*
app.controller('LinkController', [
  '$scope', 'Share', 'ShareLink', function($scope, Share, ShareLink) {

    $scope.links = {};
    $scope.posts = Share.query();

    return $scope.posts.$promise.then(function(results) {
      return angular.forEach(results, function(post) {
        return $scope.links[post.id] = ShareLink.query({
          share_id: post.id
        });
      });



    });
  }
]);
    */