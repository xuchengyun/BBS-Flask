function Paging(list_num,ali,btn){
    this.list_num=list_num;
    this.ali=ali;
    this.btn=btn;
    this.page=1;//定义一个当前页面的全局变量
    this.num=5;//每页文章数目
    this.page_num=Math.ceil(this.list_num/this.num);//根据文章数和每页显示数，向上取整算出页码数
    this.drc=[this.page-2,this.page-1,this.page,this.page+1,this.page+2];  
}