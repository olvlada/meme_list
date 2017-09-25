(function () {
    angular.module('MemeList', ['ngFileUpload']).controller('MainController', ['$scope', '$http', 'Upload', MainController]);
    function MainController($scope, $http, Upload) {
        $scope.filesForUpload = null;
        $scope.loading = false;
        $scope.dataList = [];
        $scope.uploadFile = uploadFile;
        $scope.getIconClass = getIconClass;
        $scope.exportToImage = exportToImage;
        $scope.changeImage = changeImage;

        function uploadFile() {
            if (!$scope.filesForUpload) { return null; }
            Upload.upload({
                url: 'api/upload_file',
                method: 'POST',
                data: {file: $scope.filesForUpload}
            }).then(function(response) {
                $scope.dataList = response.data.data;
            }).catch(function() {
                console.log('Error');
            });
        }

        function exportToImage() {
            $http.post(
                '/api/export_to_jpg', 
                $scope.dataList
            ).then(
                function(response) {
                    var link = document.createElement('a');
                    link.setAttribute('download', 'export.jpg');
                    link.setAttribute('href', '/export_to_jpg/' + response.data.file_code);
                    document.body.appendChild(link);
                    link.click();
                    link.parentNode.removeChild(link);
                },
                function(response) {
                    console.log('Error');
                }
            );
        }

        function exportToImageOld() {
            $scope.loading = true;
            setTimeout(function() {
                var element = document.querySelector('.content');
                html2canvas(element, {
                    useCORS: true,
                    onrendered: function(canvas) {
                        $scope.loading = false;
                        $scope.$applyAsync();
                        var link = document.createElement('a');
                        link.setAttribute('download', 'export.jpg');
                        link.setAttribute('href', canvas.toDataURL('image/jpeg', 0.5).replace('image/jpeg', 'image/octet-stream'));
                        document.body.appendChild(link);
                        link.click();
                        link.parentNode.removeChild(link);
                    }
                });
            }, 100);
        }

        function getIconClass(value) {
            return 'icon-' + value.toLowerCase().split(' ').join('-');
        }

        function changeImage(files, attr, dataItem) {
            if (files && files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    dataItem[attr] = e.target.result;
                    $scope.$applyAsync();
                };
                reader.readAsDataURL(files[0]);
            }
        }
    }
})();
