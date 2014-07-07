var callrecords;
var CallRecord = Backbone.Model.extend({idAttribute: "_id"});

var CallRecords = Backbone.PageableCollection.extend({
  model: CallRecord,
  url: "http://localhost:8000/api/v1/callrecords",
  state: {
    pageSize: 20,
  },
  queryParams:{
    pageSize: "limit",
    currentPage: null,
    Page:null,
    order_by: function(){
      return this.state.order;
    },
    offset: function () { return this.state.currentPage * this.state.pageSize; },
  }, 

  parseState: function (resp, queryParams, state, options) {
    return {totalRecords: resp.meta.total_count};
  },

  parseRecords: function (resp, options) {
    return resp.objects;
  }

});

 callrecords = new CallRecords();

//fetch the collection and define backgrid n paginator in callback
callrecords.fetch({reset:true}).done(function(data){
  var pref = data.pref;
  var order_pref = data.order_pref;
  var default_columns_pref = {
        "callerph": {name:"callerph", label:"callerph",cell: "string", sortable:false},
        "sr_number": {name:"sr_number", label:"sr_number", cell:"string", sortable:false},
        "callid": {name:"callid", label:"callid", cell:"string", sortable:false},
        "start_time": {name:"start_time", label:"start_time", cell:"datetime"},
        "voiceid": {name:"voiceid", label:"voiceid", cell:"string", sortable:false},
        "duration": {name:"duration", label:"duration", cell:"integer"},
        "destination": {name:"destination", label:"destination", cell:"string", sortable:false},
        "billed_pulses": {name:"billed_pulses", label:"billed_pulses", cell:"integer"},
        "ftype": {name:"ftype", label:"ftype", cell:"string", sortable:false},
        "filepath": {name:"filepath", label:"filepath", cell:"string", sortable:false},
        "extension": {name:"extension", label:"extension", cell:"integer", sortable:false},
        "ruleid": {name:"ruleid", label:"ruleid", cell:"integer", sortable:false},
        "is_outgoing": {name:"is_outgoing", label:"is_outgoing", cell:"string", sortable:false},
        "coins_deducted": {name:"coins_deducted", label:"coins_deducted", cell:"integer"},
  };

  var columns = [];

  //maintain order of columns
  for(i=0;i<order_pref.length;i++){
    columns.push(default_columns_pref[order_pref[i]]);
  }
  
  //show columns as per saved preference
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