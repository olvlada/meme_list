(function () {
    angular.module('MemeList', ['ngFileUpload']).controller('MainController', ['$scope', 'Upload', MainController]);
    function MainController($scope, Upload) {
        $scope.filesForUpload = null;
        $scope.dataList = [];
        $scope.uploadFile = uploadFile;
        $scope.getIconClass = getIconClass;

        function uploadFile() {
            if (!$scope.filesForUpload) { return null; }
            Upload.upload({
                url: 'api/upload_file',
                method: 'POST',
                data: {file: $scope.filesForUpload}
            }).then(function(response) {
                $scope.dataList = response.data.data;
            }).catch(function() {
                console.log('!!! error');
            });
        }

        function getIconClass(value) {
            return 'icon-' + value.toLowerCase().split(' ').join('-');
        }

        $scope.test = 187;
    }
})();
