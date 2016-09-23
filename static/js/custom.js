

$(function () {

    var data = [];
    var idInit = 0;
    $.fn.editable.defaults.mode = 'inline';
    $('.select2').select2({
        tags: true
    });

    $('#addHierarchy').click(function () {
        var columns = [];
        var dataTable = $('#dataTableId thead tr th .th-inner');
        dataTable.each(function () {
            var cellText = $(this).html().trim();
            columns.push(cellText);
        });
        var htmlElement = $('#hierarquias');
        var idDivWrapper = 'hierarchyWrapper' + idInit;
        htmlElement.append('<div id="' + idDivWrapper + '" class="col-md-6 hierarchyWrapper"> </div>');
        var newHtmlElement = $('#' + idDivWrapper + '');
        var idSelect = 'selectHierarchy' + idInit;
        var idButtonAdd = 'selectButton' + idInit;
        var idButtonDelete = 'deleteButton' + idInit;
        var options = '';
        for (i = 0; i < columns.length + 1; i++) {
            var option = '<option value="' + columns[i] + '">' + columns[i] + '</option>';
            options = option + options;
        }
        var treeElementWrapper = 'treeWrapper' + idInit;
        var treeElement = 'tree' + idInit;
        newHtmlElement.append('<div id="hierarquiaNameWrapper' + idInit + 'Id" class="hierarquiaNameWrapper form-group"> </div>');
        $('#hierarquiaNameWrapper' + idInit + 'Id').append('</br><label id="hierarquiaLabel' + idInit + 'Id" class="col-md-6 control-label" for="hierarquia' + idInit + '">Nome da Hierarquia</label>');
        $('#hierarquiaNameWrapper' + idInit + 'Id').append('<div id="hierarquiaDiv' + idInit + 'Id" class="col-md-6"> </div>');
        $('#hierarquiaDiv' + idInit + 'Id').append(' <input id="hierarquia' + idInit + 'Id" name="hierarquia' + idInit + 'Name" type="text" placeholder="" class="form-control input-hierarchy-name">');
        newHtmlElement.append('<div class="treeElement" id="' + treeElementWrapper + '"</div>');
        $('#' + treeElementWrapper + '').append('<div" id="' + treeElement + '"</div>');
        newHtmlElement.append('<select class="form-control selectHierarchy" id="' + idSelect + '"' + options + '</select>');
        newHtmlElement.append('<span class="btn btn-success btn-adicionar" id="' + idButtonAdd + '"> </span >');
        var button = $('#' + idButtonAdd + '');
        button.append('<i class="glyphicon glyphicon-plus"> </i> Adicionar nível');
        newHtmlElement.append('</br><span class="btn btn-danger btn-remove" id="' + idButtonDelete + '"> </span >');
        var buttonDelete = $('#' + idButtonDelete + '');
        buttonDelete.append('<i class="glyphicon glyphicon-minus"> </i> Remover hierarquia');
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
                        data[index].tree[0].nodes = [];
                        data[index].numberOfNodes = 0;
                    }
                    else {
                        var root = data[index].tree[0];
                        root.nodes.push(newNode);
                    }
                    data[index].numberOfNodes = data[index].numberOfNodes + 1;
                    data[index].tree[0].tags = [data[index].numberOfNodes];
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

        $('#' + idButtonDelete).click(function () {
            console.log(data);
            console.log(idSelect);
            BootstrapDialog.show({
                title: 'Atenção',
                message: 'Tem certeza que deseja excluir essa hierarquia?',
                closable: true,
                closeByBackdrop: false,
                closeByKeyboard: false,
                buttons: [
                    {
                        label: 'Não',
                        cssClass: 'btn-danger',
                        action: function (dialogRef) {
                            dialogRef.close();
                        }
                    },
                    {
                        label: 'Sim',
                        cssClass: 'btn-primary',
                        action: function (dialogRef) {
                            newHtmlElement.remove();
                            data = removeValue(data, 'select', idSelect);
                            console.log(data);
                            dialogRef.close();
                        }
                    },
                ]
            });
        });
    });


    $('#goForwardId').click(function (event) {
        var activeElement = $('ul#wizardId').find('li.active')[0];
        var activeElementId = activeElement.attributes.id.nodeValue;
        switch (activeElementId) {
            case 'step2Breadcrumb':
                var secondStep = $('#secondStepId');
                var thirdStep = $('#thirdStepId');
                var secondBreadcrumb = $('#step2Breadcrumb');
                var thirdBreadcrumb = $('#step3Breadcrumb');
                secondStep.hide();
                secondBreadcrumb.removeClass('active');
                secondBreadcrumb.addClass('disabled');
                thirdStep.show();
                thirdBreadcrumb.removeClass('disabled');
                thirdBreadcrumb.addClass('active');
                $('html, body').animate({ scrollTop: 0 }, 'fast');
                $('#goForwardId').html('Próximo <i class="fa  fa-chevron-right" ></i>');
                break;
            case 'step3Breadcrumb':
                var thirdStep = $('#thirdStepId');
                var finalStep = $('#finalStepId');
                var thirdBreadcrumb = $('#step3Breadcrumb');
                var finalBreadcrumb = $('#step4Breadcrumb');
                thirdStep.hide();
                thirdBreadcrumb.removeClass('active');
                thirdBreadcrumb.addClass('disabled');
                finalStep.show();
                finalBreadcrumb.removeClass('disabled');
                finalBreadcrumb.addClass('active');
                $('#goForwardId').html('Enviar');
                $('html, body').animate({ scrollTop: 0 }, 'fast');
                break;
            case 'step4Breadcrumb':
                sendMetadata();
                break;

        }
    });

    $('#goBackwardsId').click(function (event) {
        var activeElement = $('ul#wizardId').find('li.active')[0];
        var activeElementId = activeElement.attributes.id.nodeValue;
        switch (activeElementId) {
            case 'step2Breadcrumb':
                $('#goForwardId').html('Próximo <i class="fa  fa-chevron-right" ></i>');
                window.location.replace('/');
                $('html, body').animate({ scrollTop: 0 }, 'fast');
                break;
            case 'step3Breadcrumb':
                var secondStep = $('#secondStepId');
                var thirdStep = $('#thirdStepId');
                var secondBreadcrumb = $('#step2Breadcrumb');
                var thirdBreadcrumb = $('#step3Breadcrumb');
                secondStep.show();
                secondBreadcrumb.addClass('active');
                secondBreadcrumb.removeClass('disabled');
                thirdStep.hide();
                thirdBreadcrumb.addClass('disabled');
                thirdBreadcrumb.removeClass('active');
                $('html, body').animate({ scrollTop: 0 }, 'fast');
                $('#goForwardId').html('Próximo <i class="fa  fa-chevron-right" ></i>');
                break;
            case 'step4Breadcrumb':
                var finalStep = $('#finalStepId');
                var thirdStep = $('#thirdStepId');
                var thirdBreadcrumb = $('#step3Breadcrumb');
                var finalBreadcrumb = $('#step4Breadcrumb');
                finalStep.hide();
                finalBreadcrumb.addClass('disabled');
                finalBreadcrumb.removeClass('active');
                thirdStep.show();
                thirdBreadcrumb.addClass('active');
                thirdBreadcrumb.removeClass('disabled');
                $('#goForwardId').html('Próximo <i class="fa  fa-chevron-right" ></i>');
                $('html, body').animate({ scrollTop: 0 }, 'fast');
                break;

        }
    });

    $('body').on('click', '#closePopoverId', function (event) {
        $('[data-original-title]').popover('hide');
    });

    $('#columnsTags a').each(function (element) {
        $(this).editable({
            validate: function (value) {
                if (value === null || value === '') {
                    return 'Não são permitidos valores vazios';
                }

            }
        }, this);
        $(this).attr('title', $(this).text());
    });

    $('[data-toggle=popover]').popover({
        content: $('#preview-dataset').html(),
        html: true
    }).click(function () {
        $(this).popover('show');
        $('.popover-title').append('<button type="button" class="close">&times;</button>');
    });

    function sendMetadata() {
        if (checkValidity()) {
            var originalColumns = [];
            var aliasColumns = [];
            var tags = [];
            var hierarquias = [];

            //Colunas
            var dataTable = $('#dataTableId thead tr th .th-inner');
            dataTable.each(function () {
                var cellText = $(this).html().trim();
                originalColumns.push(cellText);
            });
            $('#columnsTags a').each(function (element) {
                var columnAliasName = $(this).html().trim();
                aliasColumns.push(columnAliasName);
            }, this);

            //Hierarquias
            if (data[0] !== undefined) {
                if (data[0].numberOfNodes > 0) {
                    for (var index in data) {
                        if (data[index].numberOfNodes > 0) {
                            var numberOfNodes = data[index].numberOfNodes;
                            var hierarquiaId = 'hierarquia' + index + 'Id';
                            var hierarchyTitle = $('#' + hierarquiaId).val();
                            var newHierarchy = {
                                'hierarchy': hierarchyTitle,
                                'levels': []
                            };
                            if (data[index].tree[0] !== undefined) {
                                var firstEntry = {
                                    "level": 0,
                                    "column": data[index].tree[0].text
                                };
                                newHierarchy.levels.push(firstEntry);
                            }
                            var nodes = data[index].tree[0].nodes;
                            for (i = 0; i < nodes.length; i++) {
                                var newEntry = {
                                    "level": i + 1,
                                    "column": nodes[i].text
                                };
                                newHierarchy.levels.push(newEntry);
                            }
                            hierarquias.push(newHierarchy);
                        }
                    }
                }
            }

            //Tags
            for (var colIndex in aliasColumns) {
                var colTags = $('#' + originalColumns[colIndex] + 'Id').select2("val");
                if (colTags !== null) {
                    var newTagEntry = {
                        "column": aliasColumns[colIndex],
                        "colTags": colTags
                    };
                    tags.push(newTagEntry);
                }
            }

            var jsonRequest = {
                "title": $('#title').val(),
                "description": $('#descriptionId').val(),
                "source": $('#source').val(),
                "email": $('#contactEmail').val(),
                "tags": tags,
                "originalColumns": originalColumns,
                "aliasColumns": aliasColumns,
                "hierarchies": hierarquias,
            };
            waitingDialog.show('Seu dataset está sendo carregado em nosso repositório!');
            $.ajax({
                type: "POST",
                url: "/upload_metadata_action/",
                data: JSON.stringify(jsonRequest),
                success: function (result) {
                    console.log(result);
                    waitingDialog.hide();
                    BootstrapDialog.show({
                        title: 'Informação',
                        message: 'Seu dataset foi carregado com sucesso!',
                        onhide: function (dialogRef) {
                            window.location.replace('/');
                            $('html, body').animate({ scrollTop: 0 }, 'fast');
                        },
                        closable: true,
                        closeByBackdrop: false,
                        closeByKeyboard: false,
                        buttons: [
                            {
                                label: 'Ok',
                                cssClass: 'btn-default',
                                action: function (dialogRef) {
                                    dialogRef.close();
                                }
                            }
                        ]
                    });

                },
                error: function (response) {
                    waitingDialog.hide();
                    if (response.status === 500) {
                        BootstrapDialog.show({
                            title: 'Atenção',
                            message: 'Ocorreu um erro. Tente novamente mais tarde ou entre em contato com os administradores.',
                            onhide: function (dialogRef) {
                                $('html, body').animate({ scrollTop: 0 }, 'fast');
                            },
                            closable: true,
                            closeByBackdrop: false,
                            closeByKeyboard: false,
                            buttons: [
                                {
                                    label: 'Ok',
                                    cssClass: 'btn-default',
                                    action: function (dialogRef) {
                                        dialogRef.close();
                                    }
                                }
                            ]
                        });
                    }
                    else if (response.status === 440) {
                        BootstrapDialog.show({
                            title: 'Atenção',
                            message: 'Sua sessão expirou. Por favor envie seu dataset novamente.',
                            onhide: function (dialogRef) {
                                window.location.replace('/upload_file');
                                $('html, body').animate({ scrollTop: 0 }, 'fast');
                            },
                            closable: true,
                            closeByBackdrop: false,
                            closeByKeyboard: false,
                            buttons: [
                                {
                                    label: 'Ok',
                                    cssClass: 'btn-default',
                                    action: function (dialogRef) {
                                        dialogRef.close();

                                    }
                                }
                            ]
                        });
                    }
                }

            });
        }
    }


    function checkValidity() {
        var titleCheck = $('#title')[0].checkValidity();
        var descriptionCheck = $('#descriptionId')[0].checkValidity();
        var sourceCheck = $('#source')[0].checkValidity();
        var emailCheck = $('#contactEmail')[0].checkValidity();
        if (!titleCheck || !descriptionCheck || !sourceCheck || !emailCheck) {
            BootstrapDialog.show({
                title: 'Erro',
                message: 'Os campos título, descrição, fonte e email são obrigatórios',
                closable: true,
                closeByBackdrop: false,
                closeByKeyboard: false,
                buttons: [
                    {
                        label: 'Ok',
                        cssClass: 'btn-default',
                        action: function (dialogRef) {
                            dialogRef.close();
                        }
                    }
                ]
            });
            return false;
        }
        return true;
    }

    function removeValue(array, name, value) {
        var newArray = $.map(array, function (v, i) {
            return v[name] === value ? null : v;
        });
        return newArray;
    }

    $('body').on('click', '#passContentSteps', function (event) {
        var activeElement = $('ul#wizardId').find('li.active')[0];
        var activeElementId = activeElement.attributes.id.nodeValue;
        switch (activeElementId) {
            case 'step1Breadcrumb':
                var content1Step = $('#content1Step');
                var content2Step = $('#content2Step');
                var firstBreadcrumb = $('#step1Breadcrumb');
                var secondBreadcrumb = $('#step2Breadcrumb');
                content1Step.fadeOut('slow');
                firstBreadcrumb.removeClass('active');
                firstBreadcrumb.addClass('disabled');
                content2Step.fadeIn('slow');
                secondBreadcrumb.removeClass('disabled');
                secondBreadcrumb.addClass('active');
                break;
            case 'step2Breadcrumb':
                var content2Step = $('#content2Step');
                var content3Step = $('#content3Step');
                var secondBreadcrumb = $('#step2Breadcrumb');
                var thirdBreadcrumb = $('#step3Breadcrumb');
                content2Step.fadeOut('slow');
                secondBreadcrumb.removeClass('active');
                secondBreadcrumb.addClass('disabled');
                content3Step.fadeIn('slow');
                thirdBreadcrumb.removeClass('disabled');
                thirdBreadcrumb.addClass('active');
                break;
            case 'step3Breadcrumb':
                var content3Step = $('#content3Step');
                var content4Step = $('#content4Step');
                var thirdBreadcrumb = $('#step3Breadcrumb');
                var fourBreadcrumb = $('#step4Breadcrumb');
                content3Step.fadeOut('slow');
                thirdBreadcrumb.removeClass('active');
                thirdBreadcrumb.addClass('disabled');
                content4Step.fadeIn('slow');
                fourBreadcrumb.removeClass('disabled');
                fourBreadcrumb.addClass('active');
                var tree = [
                    {
                        text: "Região",
                        nodes: [
                            {
                                text: "Estado",
                            },
                            {
                                text: "Cidade"
                            }
                        ],
                        tags: [3]
                    },
                ];
                $('#treeElementExample').treeview({
                    data: tree,
                    levels: 10,
                    color: "#000000",
                    backColor: "#FFFFFF",
                    showTags: true,
                    emptyIcon: '',
                });
                break;
            case 'step4Breadcrumb':
                window.location.replace('/upload_file/');
                break;
        }
    });

    $('body').on('click', '#backContentSteps', function (event) {
        var activeElement = $('ul#wizardId').find('li.active')[0];
        var activeElementId = activeElement.attributes.id.nodeValue;
        switch (activeElementId) {
            case 'step2Breadcrumb':
                var content2Step = $('#content2Step');
                var content1Step = $('#content1Step');
                var secondBreadcrumb = $('#step2Breadcrumb');
                var firstBreadcrumb = $('#step1Breadcrumb');
                content2Step.fadeOut('slow');
                secondBreadcrumb.removeClass('active');
                secondBreadcrumb.addClass('disabled');
                content1Step.fadeIn('slow');
                firstBreadcrumb.removeClass('disabled');
                firstBreadcrumb.addClass('active');
                break;
            case 'step3Breadcrumb':
                var content3Step = $('#content3Step');
                var content2Step = $('#content2Step');
                var thirdBreadcrumb = $('#step3Breadcrumb');
                var secondBreadcrumb = $('#step2Breadcrumb');
                content3Step.fadeOut('slow');
                thirdBreadcrumb.removeClass('active');
                thirdBreadcrumb.addClass('disabled');
                content2Step.fadeIn('slow');
                secondBreadcrumb.removeClass('disabled');
                secondBreadcrumb.addClass('active');
                break;
            case 'step4Breadcrumb':
                var content4Step = $('#content4Step');
                var content3Step = $('#content3Step');
                var fourBreadcrumb = $('#step4Breadcrumb');
                var thirdBreadcrumb = $('#step3Breadcrumb');
                content4Step.fadeOut('slow');
                fourBreadcrumb.removeClass('active');
                fourBreadcrumb.addClass('disabled');
                content3Step.fadeIn('slow');
                thirdBreadcrumb.removeClass('disabled');
                thirdBreadcrumb.addClass('active');
                break;
        }
    });

    $("#searchButton").click(function (event) {
        var searchValues = $("#searchKeywords").val().replace(/ /g, ",");
        var requestUrl = "/api/searchmetadata/" + searchValues;

        $.ajax({
            url: requestUrl,
            type: 'GET',
            success: function (data) {
                var inHtml = "";
                var buttonId = "seeDataId";
                $.each(data, function (index, value) {
                    var idIndex = buttonId + '' + index;
                    var newItem = '<li class="list-group-item"> <div> <span class="result-title"> Título: ' + value.title + '</span>' +
                        '</br> <span class="result-description"> Descrição: ' + value.description + '</span>' +
                        '</br> <span class="result-description"> Id do Dataset: ' + value.tableId + '</span> </div></li>';
                    inHtml += newItem;
                });

                $("#searchResult").html(inHtml);
            },
            error: function (data) {
                BootstrapDialog.show({
                    title: 'Informação',
                    message: 'Não foram encontrados datasets que satisfazem os termos buscados.',
                    onhide: function (dialogRef) {
                        $("#searchResult").html('');
                    },
                    closable: true,
                    closeByBackdrop: false,
                    closeByKeyboard: false,
                    buttons: [
                        {
                            label: 'Ok',
                            cssClass: 'btn-default',
                            action: function (dialogRef) {
                                dialogRef.close();
                            }
                        }
                    ]
                });
            }
        });
    });

    $("#searchKeywords").keyup(function (event) {
        if (event.keyCode == 13) {
            $("#searchButton").click();
        }
    });
});