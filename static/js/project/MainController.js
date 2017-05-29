(function () {
    angular.module('MemeList', ['ngFileUpload']).controller('MainController', ['$scope', 'Upload', MainController]);
    function MainController($scope, Upload) {
        $scope.filesForUpload = null;
        $scope.loading = false;
        $scope.dataList = [];
        $scope.uploadFile = uploadFile;
        $scope.getIconClass = getIconClass;
        $scope.exportToImage = exportToImage;
        $scope.changeDomainImage = changeDomainImage;

        function uploadFile() {
            console.log($scope.filesForUpload);
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

        function exportToImage() {
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

        function changeDomainImage(files, dataItem) {
            if (files && files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    dataItem.customDomainImage = e.target.result;
                    $scope.$applyAsync();
                }
                reader.readAsDataURL(files[0]);
            }
        }

        $scope.test = 187;
    }
})();
