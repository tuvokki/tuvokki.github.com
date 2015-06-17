var app = angular.module("sampleApp", ["firebase"]);

app.controller("SampleCtrl", function($scope, $firebaseArray) {
  // Get Stored TODOs
  var todosRef = new Firebase("https://amber-fire-3343.firebaseio.com/todos");
  $scope.todos = $firebaseArray(todosRef);

  $scope.testItems = function() {
    console.log("$scope.todos", $scope.todos);
  }

  // Update the "completed" status
  $scope.changeStatus   = function (olditem) {
    var item = $scope.todos.$getRecord(olditem.$id);

    item.completed = !olditem.completed;
    $scope.todos.$save(item).then(function() {
      // item has been saved
    });
  }


  // Remove a Todo
  $scope.removeItem   = function (index, item, event) {
    // Avoid wrong removing
    if (item.$id == undefined)return;
    // Firebase: Remove item from the list
    $scope.todos.$remove(item).then(function(ref) {
      ref.key() === item.$id; // true
    });
  }


  // Add new TODO
  $scope.addItem  = function () {
    // Create a unique ID
    var timestamp = new Date().valueOf()
    $scope.todos.$add({
      timestamp: timestamp,
      name : $scope.todoName,
      completed: false
    });
    $scope.todoName = "";
  }
});