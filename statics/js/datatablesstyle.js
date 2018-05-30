$.extend( $.fn.dataTable.defaults, {
  "language": {
   "search": "<span></span> _INPUT_",
   "lengthMenu": "<span>_MENU_</span>",
   "paginate": {"sFirst": "首页","sPrevious": "上一页","sNext": "下一页","sLast": "末页" },
   "processing": "正在加载中......",
   "zeroRecords": "对不起，查询不到相关数据！",
   "emptyTable": "表中无数据存在！",
   "info": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录",
   "infoFiltered": "数据表中共为 _MAX_ 条记录"
        },"sDom": "<'row'<'col-lg-4'l><'col-lg-4'T><'col-lg-4'f>r>t<'row'<'col-lg-6'i><'col-lg-6'p>>"
 });