$(function () {

    var data = [];
    var idInit = 0;

    $('.select2').select2({
        tags: true
    });

    $('#add_hierarchy').click(function () {
        var columns = [];
        var dataTable = $('#dataTableId thead tr th .th-inner');
        dataTable.each(function () {
            var cellText = $(this).html().trim();
            columns.push(cellText);
        });
        var htmlElement = $('#hierarquias');
        var idDivWrapper = 'hierarchyWrapper' + idInit;
        htmlElement.append('<div id="' + idDivWrapper + '" class="col-md-3 hierarchyWrapper"> </div>');
        var newHtmlElement = $('#' + idDivWrapper + '');
        var idSelect = 'selectHierarchy' + idInit;
        var idButtonAdd = 'selectButton' + idInit;
        var options = '';
        for (var index in columns) {
            var option = '<option value="' + columns[index] + '">' + columns[index] + '</option>';
            options = option + options;
        }
        newHtmlElement.append('<select class="form-control selectHierarchy" id="' + idSelect + '"' + options + '</select>');
        newHtmlElement.append('<span class="btn btn-success btn-adicionar" id="' + idButtonAdd + '"> </span > ');
        var button = $('#' + idButtonAdd + '');
        button.append('<i class="glyphicon glyphicon-plus"> </i> Adicionar');
        var treeElementWrapper = 'treeWrapper' + idInit;
        var treeElement = 'tree' + idInit;
        newHtmlElement.append('<div class="treeElement" id="' + treeElementWrapper + '"</div>');
        $('#' + treeElementWrapper + '').append('<div" id="' + treeElement + '"</div>');
        options = [];
        columns = [];
        var newEntry = {
            select: idSelect,
            tree: [],
            numberOfNodes: 0
        };
        data.push(newEntry);
        idInit = idInit + 1;
        $('#' + idButtonAdd).click(function () {
            var newValue = $('#' + idSelect + '').val();
            var newNode = {
                text: newValue,
                tags: [],
            };
            var selectData = [];
            for (var index in data) {
                if (data[index].select == idSelect) {
                    if (data[index].tree.length === 0) {
                        newNode.tags = [1];
                        data[index].tree.push(newNode);
                        data[index].numberOfNodes = 1;
                    }
                    else {
                        var next = data[index].tree[0];
                        for (x = 0; x < data[index].numberOfNodes; x++) {
                            if (next.nodes === undefined) {
                                next.nodes = [];
                                next.nodes.push(newNode);
                            }
                            else {
                                next = next.nodes[0];
                            }
                        }
                        data[index].numberOfNodes = data[index].numberOfNodes + 1;
                        data[index].tree[0].tags = [data[index].numberOfNodes];
                    }
                    selectData = data[index].tree;
                }
            }
            $('#' + treeElement + '').treeview({
                data: selectData,
                levels: 10,
                color: "#000000",
                backColor: "#FFFFFF",
                showTags: true,
                emptyIcon: '',
            });
        });
    });

    $('#submitMetadataId').click(function (event) {
        var columns = [];
        var dataTable = $('#dataTableId thead tr th .th-inner');
        dataTable.each(function () {
            var cellText = $(this).html().trim();
            columns.push(cellText);
        });
        var hierarquias = [];
        if (data.length > 0) {
            for (var index in data) {
                var numberOfNodes = data[index].numberOfNodes;
                var hierarchyTitle = 'hierarchy_' + index;
                var newHierarchy = {
                    'hierarchy': hierarchyTitle,
                    'levels': []
                };
                var newEntry = {
                    "level": 0,
                    "column": data[index].tree[0].text
                };
                newHierarchy.levels.push(newEntry);
                var next = data[index].tree[0];
                for (i = 1; i < numberOfNodes + 1; i++) {
                    if (next.nodes !== undefined) {
                        newEntry = {
                            "level": i,
                            "column": next.nodes[0].text
                        };
                        newHierarchy.levels.push(newEntry);
                        next = next.nodes[0];
                    }
                }
                hierarquias.push(newHierarchy);
            }
        }
        var jsonRequest = {
            "hierarchies": hierarquias,
        };
        $.ajax({
            type: "POST",
            url: "/upload_metadata_action/",
            data: JSON.stringify(jsonRequest),
            success: function (result) {
                window.location.replace('/');
            }
        });
    });

    $('#goToThirdStepId').click(function (event) {
        var jsonRequest = {
            "title": $('#title').val(),
            "description": $('#descriptionId').val(),
            "source": $('#source').val(),
        };
        $.ajax({
            type: "POST",
            url: "/upload_third_step_action/",
            data: JSON.stringify(jsonRequest),
            success: function (result) {
                window.location.replace('/upload_third_step');
            }
        });
    });

    $('#goToFinalStepId').click(function (event) {
        var columns = [];
        var tags = [];
        var dataTable = $('#columnsId label');
        dataTable.each(function () {
            var colText = $(this).html().trim();
            columns.push(colText);
        });
        console.log(columns)
        for (var colIndex in columns) {
            var colTags = $('#' + columns[colIndex] + '').select2("val");
            if (colTags !== null) {
                var newTagEntry = {
                    "column": columns[colIndex],
                    "colTags": colTags
                };
                tags.push(newTagEntry);
            }
        }
        var jsonRequest = {
            "tags": tags,
            "columns": columns
        };
        $.ajax({
            type: "POST",
            url: "/upload_final_step_action/",
            data: JSON.stringify(jsonRequest),
            success: function (result) {
                window.location.replace('/upload_final_step');
            }
        });
    });


});