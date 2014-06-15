var CallRecord = Backbone.Model.extend({});

var CallRecords = Backbone.PageableCollection.extend({
  model: CallRecord,
  url: "http://localhost:8000/api/v1/callrecords",
  state: {
    pageSize: 20
  },
  queryParams:{
    pageSize: "limit",
    currentPage: null,
    Page:null,
    sortKey: null,
    order_by: function(){
      if(this.state.sortKey){
        var prefix="";
        if(this.state.order == -1){
          prefix="-";
        }
        return (prefix + this.state.sortKey);
      }
      else{
            return null;
      }
    }, 
    offset: function () { return this.state.currentPage * this.state.pageSize; }
  }, 

  parseState: function (resp, queryParams, state, options) {
    return {totalRecords: resp.meta.total_count};
  },

  parseRecords: function (resp, options) {
    return resp.objects;
  }

});

var callrecords = new CallRecords();

//fetch the collection and define backgrid n paginator in callback
callrecords.fetch({reset:true}).done(function(data){
  var pref = data.pref;
  var columns = [
        {name:"callerph", label:"callerph",cell: "string", sortable:false},
        {name:"sr_number", label:"sr_number", cell:"string", sortable:false},
        {name:"callid", label:"callid", cell:"string", sortable:false},
        {name:"start_time", label:"start_time", cell:"datetime"},
        {name:"voiceid", label:"voiceid", cell:"string", sortable:false},
        {name:"duration", label:"duration", cell:"integer"},
        {name:"destination", label:"destination", cell:"string", sortable:false},
        {name:"billed_pulses", label:"billed_pulses", cell:"integer"},
        {name:"ftype", label:"ftype", cell:"string", sortable:false},
        {name:"filepath",  label:"filepath", cell:"string", sortable:false},
        {name:"extension", label:"extension", cell:"integer", sortable:false},
        {name:"ruleid", label:"ruleid", cell:"integer", sortable:false},
        {name:"is_outgoing", label:"is_outgoing", cell:"string", sortable:false},
        {name:"coins_deducted", label:"coins_deducted", cell:"integer"},
    ];
  
  // show columns as per saved preference
  for(i=0;i<Object.keys(pref).length;i++){
    columns[i]['renderable'] = pref[columns[i].name];
  }

  // Initialize a new Grid instance
  var grid = new Backgrid.Grid({
    columns: columns,
    collection: callrecords,
  });

  // Render the grid and attach the Grid's root to your HTML document
  var $example = $("#example-1-result");
  $example.append(grid.render().el);


  var paginator = new Backgrid.Extension.Paginator({
    collection: callrecords
  });

  $example.after(paginator.render().el);
});