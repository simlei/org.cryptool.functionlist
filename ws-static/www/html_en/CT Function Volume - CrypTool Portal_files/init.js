var plgGdprAllCookiesDisabledByScript=!1,detectedOldIPhone=!1;if(null!==navigator.userAgent.match(/iPhone/i)){var iphone4=480==window.screen.height,iphone5=568==window.screen.height;if(iphone4||iphone5)detectedOldIPhone=!0}
var plgGdprDisableAllCookies=function(a){var g=document.cookie.split("; "),c=["cookieconsent_status"];"undefined"!==typeof gdprJSessCook&&c.push(gdprJSessCook);"undefined"!==typeof gdprJAdminSessCook&&c.push(gdprJAdminSessCook);if(gdprConfigurationOptions.allowedCookies){var b=gdprConfigurationOptions.allowedCookies.split(",");c=c.concat(b)}b=function(a){for(var b=window.location.hostname.split(".");0<b.length;){var d=encodeURIComponent(a.split(";")[0].split("=")[0])+"=; expires=Thu, 01-Jan-1970 00:00:01 GMT; domain="+
b.join(".")+" ;path=",e=location.pathname.split("/");for(document.cookie=d+"/";0<e.length;){var c=e.join("/");c||(c="/");document.cookie=d+c;e.pop()}b.shift()}};for(var d=0;d<g.length;d++){for(var e=!0,h=0;h<c.length;h++)-1!=g[d].indexOf(c[h])&&(e=!1);e&&b(g[d])}a||!gdprConfigurationOptions.blockCookieDefine||detectedOldIPhone||Object.defineProperty(document,"cookie",{get:function(){return""},set:function(){return!0}});a=gdprConfigurationOptions.externalAdvancedBlockingModeCustomAttribute?",["+gdprConfigurationOptions.externalAdvancedBlockingModeCustomAttribute+
"*=gdprlock]":"";gdprConfigurationOptions.placeholderBlockedResources?jQuery("*[src*=gdprlock],*[data-source=gdprlock]"+a).filter(function(a,b){return"script"==b.nodeName.toLowerCase()||"link"==b.nodeName.toLowerCase()?!1:!0}).replaceWith('<div class="gdprlock-placeholder"><div class="gdprlock-placeholder-text">'+gdprConfigurationOptions.placeholderBlockedResourcesText+"</div></div>"):jQuery("*[src*=gdprlock],*[data-source=gdprlock]"+a).remove();plgGdprAllCookiesDisabledByScript=!0};
(function(){if("undefined"!==typeof gdpr_unset_categories_cookies)for(var a=0;a<gdpr_unset_categories_cookies.length;a++)for(var g=gdpr_unset_categories_cookies[a],c=window.location.hostname.split(".");0<c.length;){var b=encodeURIComponent(g.split(";")[0].split("=")[0])+"=; expires=Thu, 01-Jan-1970 00:00:01 GMT; domain="+c.join(".")+" ;path=",d=location.pathname.split("/");for(document.cookie=b+"/";0<d.length;){var e=d.join("/");e||(e="/");document.cookie=b+e;d.pop()}c.shift()}})();
gdprConfigurationOptions.lawByCountry||("opt-in"!=gdprConfigurationOptions.complianceType||localStorage.getItem("hasConsented")||localStorage.getItem("setConsentedCookie")||plgGdprDisableAllCookies(),"opt-out"==gdprConfigurationOptions.complianceType&&localStorage.getItem("hasDeclined")&&plgGdprDisableAllCookies());
jQuery(function(a){if(!plgGdprAllCookiesDisabledByScript){var g=gdprConfigurationOptions.externalAdvancedBlockingModeCustomAttribute?",["+gdprConfigurationOptions.externalAdvancedBlockingModeCustomAttribute+"*=gdprlock]":"";gdprConfigurationOptions.placeholderBlockedResources?jQuery("*[src*=gdprlock],*[data-source=gdprlock]"+g).filter(function(a,d){return"script"==d.nodeName.toLowerCase()||"link"==d.nodeName.toLowerCase()?!1:!0}).replaceWith('<div class="gdprlock-placeholder"><div class="gdprlock-placeholder-text">'+
gdprConfigurationOptions.placeholderBlockedResourcesText+"</div></div>"):jQuery("*[src*=gdprlock],*[data-source=gdprlock]"+g).remove()}window.gdprIsCookieConsentPresent=function(a){a=("; "+document.cookie).split("; "+a+"=");return 2!=a.length?void 0:a.pop().split(";").shift()}("cookieconsent_status");var c=function(){var b=a("iframe").length,d=!!navigator.mozGetUserMedia;gdprConfigurationOptions.blockExternalCookiesDomains&&b&&d&&localStorage.setItem("refreshIframeCache",!0);if(gdpr_enable_log_cookie_consent){if("opt-in"==
gdprConfigurationOptions.complianceType)var e=localStorage.getItem("hasConsented");else"opt-out"==gdprConfigurationOptions.complianceType&&(e=!localStorage.getItem("hasDeclined"));a.ajax({type:"POST",url:gdpr_ajax_livesite+"index.php?option=com_gdpr&task=user.processGenericCookieCategories",data:{gdpr_generic_cookie_consent:e?1:0}}).then(function(){window.location.reload()})}else setTimeout(function(){window.location.reload()},0)};a(document).on("click","a.cc-allow",function(b){"opt-out"==gdprConfigurationOptions.complianceType&&
localStorage.getItem("hasDeclined")&&(localStorage.removeItem("hasDeclined"),localStorage.removeItem("hasDenyMessage"),localStorage.removeItem("hasExplititDeclinedAll"),localStorage.setItem("setAllowRevokedCookie",!0),c());"opt-out"!=gdprConfigurationOptions.complianceType||localStorage.getItem("hasFirstDeclined")||a.ajax({type:"POST",url:gdpr_ajax_livesite+"index.php?option=com_gdpr&task=user.processGenericCookieCategories",data:{gdpr_generic_cookie_consent:1}})});localStorage.getItem("refreshIframeCache")&&
(a("iframe").each(function(b,d){b=a(d).clone();a(d).after(b).remove()}),localStorage.getItem("setConsentedCookie")||localStorage.removeItem("refreshIframeCache"));window.cookieconsent.initialise({type:gdprConfigurationOptions.complianceType,layout:gdprConfigurationOptions.toolbarLayout,theme:gdprConfigurationOptions.toolbarTheme,position:gdprConfigurationOptions.toolbarPosition,revokeposition:gdprConfigurationOptions.revokePosition,container:document.querySelector(gdprConfigurationOptions.containerSelector),
palette:{popup:{background:gdprConfigurationOptions.popupBackground,text:gdprConfigurationOptions.popupText,link:gdprConfigurationOptions.popupLink,effect:gdprConfigurationOptions.popupEffect},button:{background:gdprConfigurationOptions.buttonBackground,border:gdprConfigurationOptions.buttonBorder,text:gdprConfigurationOptions.buttonText},highlight:{background:gdprConfigurationOptions.highlightBackground,border:gdprConfigurationOptions.highlightBorder,text:gdprConfigurationOptions.highlightText},
highlightDismiss:{background:gdprConfigurationOptions.highlightDismissBackground,border:gdprConfigurationOptions.highlightDismissBorder,text:gdprConfigurationOptions.highlightDismissText},highlightOpacity:{opacity:gdprConfigurationOptions.highlightOpacity},buttonall:{background:gdprConfigurationOptions.allowallButtonBackground,border:gdprConfigurationOptions.allowallButtonBorder,text:gdprConfigurationOptions.allowallButtonText},buttonSettings:{background:gdprConfigurationOptions.toggleCookieSettingsButtonBackground,
border:gdprConfigurationOptions.toggleCookieSettingsButtonBorder,text:gdprConfigurationOptions.toggleCookieSettingsButtonText}},revokable:!!gdprConfigurationOptions.revokable,location:!!gdprConfigurationOptions.lawByCountry,law:{regionalLaw:!gdprConfigurationOptions.lawByCountry},showLink:!!gdprConfigurationOptions.showLinks,static:!gdprConfigurationOptions.toolbarPositionmentType,dismissOnScroll:gdprConfigurationOptions.dismissOnScroll,dismissOnTimeout:gdprConfigurationOptions.dismissOnTimeout,animateRevokable:!!gdprConfigurationOptions.hideRevokableButton,
onInitialise:function(a){"opt-out"==gdprConfigurationOptions.complianceType&&localStorage.getItem("setAllowRevokedCookie")&&(this.setStatus("allow",!0),localStorage.removeItem("setAllowRevokedCookie"))},content:{header:gdprConfigurationOptions.headerText,message:gdprConfigurationOptions.messageText,dismiss:gdprConfigurationOptions.dismissText,allow:gdprConfigurationOptions.allowText,deny:gdprConfigurationOptions.denyText,allowall:gdprConfigurationOptions.allowallText,link:gdprConfigurationOptions.cookiePolicyLinkText,
href:gdprConfigurationOptions.cookiePolicyLink,privacylink:gdprConfigurationOptions.privacyPolicyLinkText,privacyhref:gdprConfigurationOptions.privacyPolicyLink},onStatusChange:function(b,d){d=this.options.type;var e=this.hasConsented();if("opt-in"==d&&(e||a("a.cc-btn",this.element).hasClass("cc-allow"))&&"allow"==b){var h=localStorage.getItem("hasConsented"),l=localStorage.getItem("hasExplititDeclinedAll"),f={hasConsented:!0,timestamp:(new Date).getTime()};localStorage.setItem("hasConsented",JSON.stringify(f));
plgGdprAllCookiesDisabledByScript&&localStorage.setItem("setConsentedCookie",!0);localStorage.removeItem("hasExplititDeclinedAll");gdprConfigurationOptions.preserveLockedCategories?a("input.cc-cookie-checkbox:not([readonly])").attr("disabled",!1):a("input.cc-cookie-checkbox").attr("disabled",!1);if(gdprConfigurationOptions.disableFirstReload){f=!1;var g=parseInt(localStorage.getItem("autoActivateOnNextPage")),k=!localStorage.getItem("hasFirstAccepted");if(!k||1==g||l)h&&gdprIsCookieConsentPresent||
(f=!0,c());gdpr_enable_log_cookie_consent&&k&&!f&&a.ajax({type:"POST",url:gdpr_ajax_livesite+"index.php?option=com_gdpr&task=user.processGenericCookieCategories",data:{gdpr_generic_cookie_consent:1}});k&&(f={hasFirstAccepted:!0,timestamp:(new Date).getTime()},localStorage.setItem("hasFirstAccepted",JSON.stringify(f)))}else h&&gdprIsCookieConsentPresent||c()}"opt-in"!=d||e&&!a("a.cc-btn",this.element).hasClass("cc-deny")||"deny"!=b||(h=localStorage.getItem("hasConsented"),localStorage.removeItem("hasConsented"),
localStorage.removeItem("setConsentedCookie"),f={hasDeclined:!0,timestamp:(new Date).getTime()},localStorage.setItem("hasFirstDeclined",JSON.stringify(f)),localStorage.setItem("hasExplititDeclinedAll",JSON.stringify(f)),this.setStatus("deny",!0),gdprConfigurationOptions.preserveLockedCategories?a("input.cc-cookie-checkbox:not([readonly])").attr("disabled",!0):a("input.cc-cookie-checkbox").attr("disabled",!0),h?c():a.ajax({type:"POST",url:gdpr_ajax_livesite+"index.php?option=com_gdpr&task=user.processGenericCookieCategories",
data:{gdpr_generic_cookie_consent:0}}).then(function(){gdprConfigurationOptions.reloadOnfirstDeclineall&&"undefined"!==typeof gdprUseCookieCategories&&window.location.reload()}));"opt-out"!=d||e||localStorage.getItem("hasDeclined")||(plgGdprDisableAllCookies(!0),f={hasDeclined:!0,timestamp:(new Date).getTime()},localStorage.setItem("hasDeclined",JSON.stringify(f)),localStorage.setItem("hasFirstDeclined",JSON.stringify(f)),localStorage.setItem("hasExplititDeclinedAll",JSON.stringify(f)),gdprConfigurationOptions.preserveLockedCategories?
a("input.cc-cookie-checkbox:not([readonly])").attr("disabled",!0):a("input.cc-cookie-checkbox").attr("disabled",!0),c());gdprConfigurationOptions.denyMessageEnabled&&"allow"==b&&localStorage.removeItem("hasDenyMessage")},onPopupOpen:function(b){"opt-in"!=gdprConfigurationOptions.complianceType&&"opt-out"!=gdprConfigurationOptions.complianceType||!gdprConfigurationOptions.autoAcceptOnNextPage||b||localStorage.getItem("hasExplititDeclinedAll")||(b=localStorage.getItem("autoActivateOnNextPage"),2==parseInt(b)?
(localStorage.setItem("autoActivateOnNextPage",1),"opt-in"==gdprConfigurationOptions.complianceType?(a("div.cc-window.cc-banner,div.cc-window.cc-floating").hide(),a("a.cc-btn.cc-allow").trigger("click")):"opt-out"==gdprConfigurationOptions.complianceType&&setTimeout(function(){a("a.cc-btn.cc-allow").trigger("click")},100)):b||localStorage.setItem("autoActivateOnNextPage",2))}});if(gdprConfigurationOptions.trackExistingCheckboxSelectors)a(gdprConfigurationOptions.trackExistingCheckboxSelectors).on("change",
function(b){parentForm=a(b.target).parents("form");var d={url:a(location).attr("href"),formid:parentForm.attr("id"),formname:parentForm.attr("name"),formfields:{}};a(this).is(":checked")&&0!=parseInt(a(this).val())?(b=gdprConfigurationOptions.trackExistingCheckboxConsentLogsFormfields.split(","),b=b.map(function(a,b){return a.trim()}),a.each(b,function(b,c){b=a("input[name*="+c+"]:not(:hidden), input[id*="+c+"]:not(:hidden), textarea[name*="+c+"], textarea[id*="+c+"]",parentForm);b.length&&a.each(b,
function(b,c){(b=a(c).attr("id"))||(b=a(c).attr("name"));b=b.replace(/[-_]/gi," ");b=b.replace(/[\[\]]/gi,"");b=b.replace("jform","");b=b.trim();c=a(c).val();d.formfields[b]=c})}),a.ajax({type:"POST",url:gdpr_ajax_livesite+"index.php?option=com_gdpr&task=user.storeConsent&format=raw",data:d})):a.ajax({type:"POST",url:gdpr_ajax_livesite+"index.php?option=com_gdpr&task=user.deleteConsent&format=raw",data:d})})});