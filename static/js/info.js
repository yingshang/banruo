function getParameterByName(name, url) {
    if (!url) {
        url = window.location.href;
    }
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}



$(function () {
    var current_tab = '';
    var c_tab = getParameterByName('t');
    if (c_tab !== null && c_tab !== '' && ['inf', 'vul'].indexOf(c_tab) >= 0) {
        current_tab = c_tab;
        $(".nav-tabs li").removeClass('active');
        $("a[data-id=" + c_tab + "]").parent('li').addClass('active');
        $(".tab-pane").removeClass('active');
        $('#' + c_tab).addClass('active');
    }
    var vulnerabilities_list = {
        page: 1,
        vid: null,
        cm_code: null,
        init: function () {
            var vid = getParameterByName('vid');
            if (vid !== null && vid > 0) {
                vulnerabilities_list.vid = vid;
            }
            this.get();
            this.listen();
        },
        listen: function () {
            // filter submit button
            $('.filter_btn').on('click', function () {
                vulnerabilities_list.page = 1;
                vulnerabilities_list.pushState();
                vulnerabilities_list.get();
                vulnerabilities_list.trigger_filter();
            });

            // filter setting
            $('.filter_setting').on('click', function () {
                vulnerabilities_list.trigger_filter();
            });
        },
        detail: function (vid) {
            $('.vulnerabilities_list li').removeClass('active');
            $('li[data-id=' + vid + ']').addClass('active');
            // hide loading
            $('.CodeMirror .cm-loading').hide();
            vid = Number(vid);
            var token = $('#search_target').val();
            var data = vul_list_origin.vulnerabilities[vid - 1];

            $.ajax({
                type: 'POST',
                url: 'api/vuldetail',
                data: {id: getParameterByName('id'), vid: getParameterByName('vid')},
                success: function (result) {
                    if (result.code === 1001) {
                        data.code_content = result.result.file_content;
                        data.language = result.result.extension;
                        // 对二进制文件情况进行处理，将行数置为 1
                        if (data.code_content === "This is a binary file.") {
                            data.line_number = 1;
                        }
                        $('#code').val(data.code_content);
                        // Highlighting param
                        vulnerabilities_list.cm_code.setOption("mode", data.language);
                        if (vulnerabilities_list.cm_code !== null) {
                            var doc = vulnerabilities_list.cm_code.getDoc();
                            doc.setValue(data.code_content);
                        }
                        vulnerabilities_list.cm_code.operation(function () {
                            // panel
                            $('.v-path').text(data.file_path + ':' + data.line_number);
                            $('.v-id').text('漏洞-' + vid);
                            $('.v-language').text(data.language);

                            // widget
                            function init_widget() {
                                var lis = $('.widget-trigger li');

                                $('.v-level').text(data.level);
                                $('.v-type').text(data.rule_name);
                                $('.v-describe').text(data.describe);
                                $('.v-Recommendation').text(data.Recommendation);
                                // $('.v-rule').text(data.match_result);
                            }

                            init_widget();
                            var widget_trigger_line = $('.widget-trigger').clone().get(0);
                            var widget_config = {
                                coverGutter: false,
                                noHScroll: false
                            };
                            vulnerabilities_list.cm_code.addLineWidget(data.line_number - 1, widget_trigger_line, widget_config);
                            var h = vulnerabilities_list.cm_code.getScrollInfo().clientHeight;
                            var coords = vulnerabilities_list.cm_code.charCoords({
                                line: data.line_number,
                                ch: 0
                            }, "local");
                            vulnerabilities_list.cm_code.scrollTo(null, (coords.top + coords.bottom - h) / 2);
                            // set cursor
                            doc.setCursor({line: data.line_number - 1, ch: 0});

                        });

                        $('input[name=vulnerability_path]').val(data.file_path);
                        $('input[name=rule_id]').val(data.id);
                        $('input[name=vid]').val(data.id);

                    } else {
                        alert(result.msg);
                    }
                }
            });
        },
        filter_url: function () {
            var search_filter_url = '';

            var sr = $('#search_rule').val();
            if (sr !== 'all' ) {
                search_filter_url += '&sr=' + sr;
            }
            var sl = $('#search_level').val();
            if (sl !== 'all' ) {
                search_filter_url += '&sl=' + sl;
            }
            return search_filter_url;
        },
        pushState: function () {
            var v = '';
            if (vulnerabilities_list.vid !== null) {
                v = '&vid=' + vulnerabilities_list.vid;
            }

            var token = '';
            if (token !== null) {
                token = '&token=' + getParameterByName('token');
            }

            var id = '';
            if (id !==null)
            {
                id = '&id=' +getParameterByName('id');
            }

            if (current_tab === '') {
                current_tab = 'inf';
            }
            url = '?t=' + current_tab + token  + id + vulnerabilities_list.filter_url() + v;
            window.history.pushState("CobraState", "Cobra", url);
        },
        get: function (on_filter) {
            if (vulnerabilities_list.cm_code === null) {
                vulnerabilities_list.cm_code = CodeMirror.fromTextArea(document.getElementById("code"), {
                    mode: 'php',
                    theme: 'material',
                    lineNumbers: true,
                    lineWrapping: true,
                    matchBrackets: true,
                    styleActiveLine: true,
                    matchTags: {bothTags: true},
                    indentUnit: 4,
                    indentWithTabs: true,
                    foldGutter: true,
                    scrollbarStyle: 'simple',
                    autofocus: false,
                    readOnly: true,
                    highlightSelectionMatches: {showToken: /\w/, annotateScrollbar: true},
                    gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"]
                });

                // panel
                var numPanels = 0;
                var panels = {};

                function makePanel(where, content) {
                    var node = document.createElement("div");
                    var id = ++numPanels;
                    var widget;
                    node.id = "panel-" + id;
                    node.className = "cm_panel widget-" + where;
                    node.innerHTML = content;
                    return node;
                }

                function addPanel(where, content) {
                    var node = makePanel(where, content);
                    panels[node.id] = vulnerabilities_list.cm_code.addPanel(node, {position: where, stable: true});
                }

                var content_bottom = '<span class="v-id">MVE-0001</span>' + '<span class="v-language">PHP</span>';
                addPanel('bottom', content_bottom);
                var content_top = '<strong class="v-path">/this/is/a/demo/code.php:1</strong>';
                addPanel('top', content_top);

                // full screen
                $('.full-screen').click(function () {
                    $('.exit-full-screen').show();
                    vulnerabilities_list.cm_code.setOption("fullScreen", !vulnerabilities_list.cm_code.getOption("fullScreen"));
                });
                $('.exit-full-screen').click(function () {
                    $('.exit-full-screen').hide();
                    if (vulnerabilities_list.cm_code.getOption("fullScreen")) vulnerabilities_list.cm_code.setOption("fullScreen", false);
                });

                // ESC exit full screen
                $('body').on('keydown', function (evt) {
                    if (evt.keyCode === 27) {
                        if (vulnerabilities_list.cm_code.getOption("fullScreen")) vulnerabilities_list.cm_code.setOption("fullScreen", false);
                    }
                    evt.stopPropagation();
                });
            }

            vulnerabilities_list.pushState();

            // load vulnerabilities list

            $.ajax({
                type: 'POST',
                url: 'api/vullist',
                data: {id: getParameterByName('id')},

                success: function (result) {
                    if (result.code === 1001) {
                        vul_list_origin = result.result.scan_data;
                        rule_filter = result.result.rule_filter;
                        // rule filter
                        $('#search_rule').empty();
                        $('#search_rule').append('<option value="all">All</option>');
                        for (var key in rule_filter) {
                            $('#search_rule').append('<option value="' + rule_filter[key] + '">' + rule_filter[key] + '</option>');
                        }

                        // Search vulnerability type
                        if (on_filter === false || typeof on_filter === 'undefined') {
                            // Search rule
                            var sr = getParameterByName('sr');
                            if (sr !== null ) {
                                $('#search_rule').val(sr);
                            }
                            // Search level
                            var sl = getParameterByName('sl');
                            if (sl !== null) {
                                $('#search_level').val(sl);
                            }
                            // Search target

                        }

                        // vulnerabilities list
                        var list = vul_list_origin.vulnerabilities;
                        var list_html = '';

                        var id = 0;
                        for (var i = 0; i < list.length; i++) {
                            // search rule
                            if (sr !== null) {
                                if (list[i].rule_name !== sr) {
                                    continue;
                                }
                            }
                            // search level
                            if (sl !== null ) {
                                if (list[i].level !== sl) {
                                    continue;
                                }
                            }
                            var line = '';
                            if (list[i].line_number !== 0) {
                                line = ':' + list[i].line_number;
                            }
                            list_html = list_html + '<li data-id="' + (i + 1) + '" class="' + list[i].level + '"' +
                                ' data-start="1" data-line="1">' +
                                '<strong>漏洞号-' + (i + 1) + '</strong><br><span>' + list[i].file_path + line + '</span><br>' +
                                '<span class="issue-information">' +
                                '<small>' +
                                ' 漏洞标题： ' + list[i].rule_name +
                                '</small>' +
                                '</span>' +
                                '</li>';
                        }
                        if (list_html.length === 0) {
                            $(".vulnerabilities_list").html('<li><h3 style="text-align: center;margin: 200px auto;">Wow, no vulnerability was detected :)</h3></li>');
                        } else {
                            $('.vulnerabilities_list').html(list_html);
                        }

                        // current vulnerability
                        var vid = getParameterByName('vid');
                        if (vid !== null && vid > 0) {
                            vulnerabilities_list.detail(vid);
                        }

                        // vulnerabilities list detail
                        $('.vulnerabilities_list li').off('click').on('click', function () {
                            // loading
                            $('.CodeMirror').prepend($('.cm-loading').show().get(0));

                            vulnerabilities_list.vid = $(this).attr('data-id');
                            vulnerabilities_list.pushState();

                            vulnerabilities_list.detail(vulnerabilities_list.vid);
                        });
                    } else {
                        alert(result.msg);
                    }
                }
            });


        },
        trigger_filter: function () {
            if ($(".filter").is(":visible") === true) {
                $('.filter').hide();
                $('.vulnerabilities_list').show();
            } else {
                $('.vulnerabilities_list').hide();
                $('.filter').show();
            }
        }
    };
    vulnerabilities_list.init();

    // tab
    $(".nav-tabs li a").on('click', function () {
        var id = $(this).attr('data-id');
        current_tab = id;
        $(".nav-tabs li").removeClass('active');
        $(this).parent('li').addClass('active');
        $(".tab-pane").removeClass('active');
        $('#' + id).addClass('active');
        vulnerabilities_list.pushState();
    });
});