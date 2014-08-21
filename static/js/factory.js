// create a factory or service
var app = angular.module('share.api', ['ngResource']);


app.factory('User', [
  '$resource', function($resource) {
    return $resource('/api/users/:username', {
      username: '@username'
    });
  }
]);

app.factory('Share', [
  '$resource', function($resource) {
    return $resource('/api/shares/:id', {
      id: '@id'
    });
  }
]);

app.factory('UserShare', [
  '$resource', function($resource) {
    return $resource('/api/users/:username/shares/:id');
  }
]);

app.factory('ShareLink', [
  '$resource', function($resource) {
    return $resource('/api/shares/:share_id/links/:id', {}, {
        get: {
            method: "GET",
            cache: true
        }
    });
  }
]);

/*
app.factory('Tag', [
  '$resource', function($resource) {
    return $resource('/api/tags/:id', {
      id: '@id'
    });
  }
]);



app.factory('ShareTag', [
  '$resource', function($resource) {
    return $resource('/api/shares/:share_id/tags/:id');
    //return $resource('/api/shares/:id/tags');
   // return $resource('/api/shares/1/tags', {
   //   id: '@id'
  //  });
  }
]);

app.factory('ShareLink', [
  '$resource', function($resource) {
    return $resource('/api/shares/:share_id/links/:id', {}, {
        get: {
            method: "GET",
            cache: true
        }
    });
  }
]);

*/
// http://stackoverflow.com/a/14094714


// http://stackoverflow.com/questions/14117653/how-to-cache-an-http-get-service-in-angularjs CACHING
/// end of service api