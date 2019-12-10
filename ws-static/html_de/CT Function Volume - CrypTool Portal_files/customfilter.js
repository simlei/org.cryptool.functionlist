jQuery.fn.dataTableExt.afnFiltering.push(
    function( oSettings, aData, iDataIndex ) {
	//if aData[0] matches and aData[5 or 6 or 7 or 8] visible OR aData[5|6|7|8] matches and is visible 
  	var oTable = jQuery('#myTable').dataTable();

        var bVis5 = oTable.fnSettings().aoColumns[5].bVisible; 
        var bVis6 = oTable.fnSettings().aoColumns[6].bVisible; 
        var bVis7 = oTable.fnSettings().aoColumns[7].bVisible; 
        var bVis8 = oTable.fnSettings().aoColumns[8].bVisible; 
	var cs = jQuery('#custom_search').val().toLowerCase(); 
	var cat = jQuery('#cat_selector').val().toLowerCase();

if(cs.length >= 0) {
if ((aData[5].toLowerCase().indexOf(cs)>=0) && bVis5 && aData[5].length>0)
        {
		 if (cat.length==0 || aData[9].toLowerCase().indexOf(cat)>=0){
                	return true;
        	}

        }
        else if ((aData[6].toLowerCase().indexOf(cs)>=0) && bVis6 && aData[6].length>0)
        {
		if (cat.length==0 ||aData[9].toLowerCase().indexOf(cat)>=0){
                	return true;
        	}

        }
        else if ((aData[7].toLowerCase().indexOf(cs)>=0) && bVis7 && aData[7].length>0)
        {
	        if (cat.length==0 ||aData[9].toLowerCase().indexOf(cat)>=0){
                	return true;
        	}

	}
        else if ((aData[8].toLowerCase().indexOf(cs)>=0) && bVis8 && aData[8].length>0)
        {
		if (cat.length==0 ||aData[9].toLowerCase().indexOf(cat)>=0){
                	return true;
        	}
        }else if ((aData[0].toLowerCase().indexOf(cs)>=0) && (((aData[1].length>0) && bVis5) ||  ((aData[2].length>0) && bVis6) || ((aData[3].length>0) && bVis7) || ((aData[4].length>0) && bVis8))) {
		if (cat.length==0 ||aData[9].toLowerCase().indexOf(cat)>=0){
                	return true;
        	}
	}
       	 return false;
	
    }else { return true;}
}
);
