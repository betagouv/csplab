import{i as e,r as t}from"./preload-helper-DVWsqyFp.js";import{$ as n,B as r,D as i,F as a,G as o,H as s,It as c,R as l,V as u,at as d,ct as f,ft as p,ht as m,kt as h,nt as g,st as _,vt as v,zt as y}from"./iframe-CCJ5pCxD.js";import{n as ee,t as te}from"./_plugin-vue_export-helper-BuTp77SO.js";import{n as ne,t as re}from"./CspIcon-CoQmeH3p.js";import{n as ie,t as ae}from"./CspButton-D1-r457y.js";function b(e){"@babel/helpers - typeof";return b=typeof Symbol==`function`&&typeof Symbol.iterator==`symbol`?function(e){return typeof e}:function(e){return e&&typeof Symbol==`function`&&e.constructor===Symbol&&e!==Symbol.prototype?`symbol`:typeof e},b(e)}var oe=e((()=>{}));function se(e,t){if(b(e)!=`object`||!e)return e;var n=e[Symbol.toPrimitive];if(n!==void 0){var r=n.call(e,t||`default`);if(b(r)!=`object`)return r;throw TypeError(`@@toPrimitive must return a primitive value.`)}return(t===`string`?String:Number)(e)}var ce=e((()=>{oe()}));function le(e){var t=se(e,`string`);return b(t)==`symbol`?t:t+``}var ue=e((()=>{oe(),ce()}));function x(e,t,n){return(t=le(t))in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var S=e((()=>{ue()}));function de(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function fe(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?de(Object(n),!0).forEach(function(t){x(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):de(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function pe(e,t){var n=t.element,r=t.input,i=t.allowedEdges,a={x:r.clientX,y:r.clientY},o=n.getBoundingClientRect(),s=i.map(function(e){return{edge:e,value:he[e](o,a)}}).sort(function(e,t){return e.value-t.value})[0]?.edge??null;return fe(fe({},e),{},x({},C,s))}function me(e){return e[C]??null}var he,C,ge=e((()=>{S(),he={top:function(e,t){return Math.abs(t.y-e.top)},right:function(e,t){return Math.abs(e.right-t.x)},bottom:function(e,t){return Math.abs(e.bottom-t.y)},left:function(e,t){return Math.abs(t.x-e.left)}},C=Symbol(`closestEdge`)}));function _e(e){var t=e.startIndex,n=e.closestEdgeOfTarget,r=e.indexOfTarget,i=e.axis;if(t===-1||r===-1||t===r)return t;if(n==null)return r;var a=i===`vertical`&&n===`bottom`||i===`horizontal`&&n===`right`;return t<r?a?r:r-1:a?r+1:r}var ve=e((()=>{})),ye,be=e((()=>{ye=1e3}));function xe(){var e=document.createElement(`div`);return e.setAttribute(`role`,`status`),Object.assign(e.style,Te),document.body.append(e),e}function Se(){return w===null&&(w=xe()),w}function Ce(){E!==null&&clearTimeout(E),E=null}function we(e){Se(),Ce(),E=setTimeout(function(){E=null;var t=Se();t.textContent=e},ye)}var w,T,Te,E,Ee=e((()=>{be(),w=null,T=`1px`,Te={width:T,height:T,padding:`0`,position:`absolute`,border:`0`,clip:`rect(${T}, ${T}, ${T}, ${T})`,overflow:`hidden`,whiteSpace:`nowrap`,marginTop:`-${T}`,pointerEvents:`none`},E=null}));function De(e){if(Array.isArray(e))return e}var Oe=e((()=>{}));function ke(e,t){var n=e==null?null:typeof Symbol<`u`&&e[Symbol.iterator]||e[`@@iterator`];if(n!=null){var r,i,a,o,s=[],c=!0,l=!1;try{if(a=(n=n.call(e)).next,t===0){if(Object(n)!==n)return;c=!1}else for(;!(c=(r=a.call(n)).done)&&(s.push(r.value),s.length!==t);c=!0);}catch(e){l=!0,i=e}finally{try{if(!c&&n.return!=null&&(o=n.return(),Object(o)!==o))return}finally{if(l)throw i}}return s}}var Ae=e((()=>{}));function je(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}var Me=e((()=>{}));function Ne(e,t){if(e){if(typeof e==`string`)return je(e,t);var n={}.toString.call(e).slice(8,-1);return n===`Object`&&e.constructor&&(n=e.constructor.name),n===`Map`||n===`Set`?Array.from(e):n===`Arguments`||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?je(e,t):void 0}}var Pe=e((()=>{Me()}));function Fe(){throw TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var Ie=e((()=>{}));function Le(e,t){return De(e)||ke(e,t)||Ne(e,t)||Fe()}var D=e((()=>{Oe(),Ae(),Pe(),Ie()})),Re=t((e=>{Object.defineProperty(e,"__esModule",{value:!0}),e.bind=void 0;function t(e,t){var n=t.type,r=t.listener,i=t.options;return e.addEventListener(n,r,i),function(){e.removeEventListener(n,r,i)}}e.bind=t})),ze=t((e=>{var t=e&&e.__assign||function(){return t=Object.assign||function(e){for(var t,n=1,r=arguments.length;n<r;n++)for(var i in t=arguments[n],t)Object.prototype.hasOwnProperty.call(t,i)&&(e[i]=t[i]);return e},t.apply(this,arguments)};Object.defineProperty(e,"__esModule",{value:!0}),e.bindAll=void 0;var n=Re();function r(e){if(e!==void 0)return typeof e==`boolean`?{capture:e}:e}function i(e,n){return n==null?e:t(t({},e),{options:t(t({},r(n)),r(e.options))})}function a(e,t,r){var a=t.map(function(t){var a=i(t,r);return(0,n.bind)(e,a)});return function(){a.forEach(function(e){return e()})}}e.bindAll=a})),O=t((e=>{Object.defineProperty(e,"__esModule",{value:!0}),e.bindAll=e.bind=void 0;var t=Re();Object.defineProperty(e,"bind",{enumerable:!0,get:function(){return t.bind}});var n=ze();Object.defineProperty(e,"bindAll",{enumerable:!0,get:function(){return n.bindAll}})})),Be,Ve=e((()=>{Be=`data-pdnd-honey-pot`}));function He(e){return e instanceof Element&&e.hasAttribute(`data-pdnd-honey-pot`)}var Ue=e((()=>{Ve()}));function We(e){var t=Le(document.elementsFromPoint(e.x,e.y),2),n=t[0],r=t[1];return n?He(n)?r??null:n:null}var Ge=e((()=>{D(),Ue()})),Ke,qe=e((()=>{Ke=2147483647})),Je,Ye=e((()=>{Je={inset:`unset`,border:`none`,padding:0,margin:0,overflow:`visible`,color:`inherit`,background:`transparent`,width:`auto`,height:`auto`}}));function k(e){var t=null;return function(){if(!t){var n=[...arguments];t={result:e.apply(this,n)}}return t.result}}var A=e((()=>{})),j,Xe=e((()=>{A(),j=k(function(){return typeof HTMLElement<`u`&&typeof HTMLElement.prototype.showPopover==`function`})}));function Ze(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function Qe(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?Ze(Object(n),!0).forEach(function(t){x(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):Ze(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function $e(e){return{x:Math.floor(e.x),y:Math.floor(e.y)}}function et(e){return{x:e.x-P,y:e.y-P}}function tt(e){return{x:Math.max(e.x,0),y:Math.max(e.y,0)}}function nt(e){return{x:Math.min(e.x,window.innerWidth-N),y:Math.min(e.y,window.innerHeight-N)}}function rt(e){var t=e.client,n=nt(tt(et($e(t))));return DOMRect.fromRect({x:n.x,y:n.y,width:N,height:N})}function it(e){var t=e.clientRect;return{left:`${t.left}px`,top:`${t.top}px`,width:`${t.width}px`,height:`${t.height}px`}}function at(e){var t=e.client,n=e.clientRect;return t.x>=n.x&&t.x<=n.x+n.width&&t.y>=n.y&&t.y<=n.y+n.height}function ot(e){var t=e.initial,n=document.createElement(`div`);n.setAttribute(Be,`true`),j()&&n.setAttribute(`popover`,`manual`);var r=rt({client:t});Object.assign(n.style,Qe(Qe({position:`fixed`},j()?Je:{zIndex:Ke}),{},{backgroundColor:`transparent`,padding:0,margin:0,boxSizing:`border-box`,pointerEvents:`auto`},it({clientRect:r}))),document.body.appendChild(n),j()&&n.showPopover();var i=(0,M.bind)(window,{type:`pointermove`,listener:function(e){r=rt({client:{x:e.clientX,y:e.clientY}}),Object.assign(n.style,it({clientRect:r}))},options:{capture:!0}});return function(e){var t=e.current;if(i(),at({client:t,clientRect:r})){n.remove();return}function a(){o(),n.remove()}var o=(0,M.bindAll)(window,[{type:`pointerdown`,listener:a},{type:`pointermove`,listener:a},{type:`focusin`,listener:a},{type:`focusout`,listener:a},{type:`dragstart`,listener:a},{type:`dragenter`,listener:a},{type:`dragover`,listener:a}],{capture:!0})}}function st(){var e=null;function t(){return e=null,(0,M.bind)(window,{type:`pointermove`,listener:function(t){e={x:t.clientX,y:t.clientY}},options:{capture:!0}})}function n(){var t=null;return function(n){var r=n.eventName,i=n.payload;if(r===`onDragStart`){var a=i.location.initial.input;t=ot({initial:e??{x:a.clientX,y:a.clientY}})}if(r===`onDrop`){var o,s=i.location.current.input;(o=t)==null||o({current:{x:s.clientX,y:s.clientY}}),t=null,e=null}}}return{bindEvents:t,getOnPostDispatch:n}}var M,N,P,ct=e((()=>{S(),M=O(),qe(),Ye(),Xe(),Ve(),N=2,P=N/2}));function lt(e){if(Array.isArray(e))return je(e)}var ut=e((()=>{Me()}));function dt(e){if(typeof Symbol<`u`&&e[Symbol.iterator]!=null||e[`@@iterator`]!=null)return Array.from(e)}var ft=e((()=>{}));function pt(){throw TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var mt=e((()=>{}));function ht(e){return lt(e)||dt(e)||Ne(e)||pt()}var gt=e((()=>{ut(),ft(),Pe(),mt()})),_t,vt=e((()=>{A(),_t=k(function(){return navigator.userAgent.includes(`Firefox`)})})),F,yt=e((()=>{A(),F=k(function(){var e=navigator.userAgent;return e.includes(`AppleWebKit`)&&!e.includes(`Chrome`)})}));function bt(e){var t=e.dragLeave;return F()?t.hasOwnProperty(I.isLeavingWindow):!1}var xt,I,St=e((()=>{xt=O(),yt(),I={isLeavingWindow:Symbol(`leaving`),isEnteringWindow:Symbol(`entering`)},(function(){if(typeof window>`u`||!F())return;function e(){return{enterCount:0,isOverWindow:!1}}var t=e();function n(){t=e()}(0,xt.bindAll)(window,[{type:`dragstart`,listener:function(){t.enterCount=0,t.isOverWindow=!0}},{type:`drop`,listener:n},{type:`dragend`,listener:n},{type:`dragenter`,listener:function(e){!t.isOverWindow&&t.enterCount===0&&(e[I.isEnteringWindow]=!0),t.isOverWindow=!0,t.enterCount++}},{type:`dragleave`,listener:function(e){t.enterCount--,t.isOverWindow&&t.enterCount===0&&(e[I.isLeavingWindow]=!0,t.isOverWindow=!1)}}],{capture:!0})})()}));function Ct(e){return`nodeName`in e}function wt(e){return Ct(e)&&e.ownerDocument!==document}var Tt=e((()=>{}));function Et(e){var t=e.dragLeave,n=t.type,r=t.relatedTarget;return n===`dragleave`?F()?bt({dragLeave:t}):r==null?!0:_t()?wt(r):r instanceof HTMLIFrameElement:!1}var Dt=e((()=>{vt(),yt(),St(),Tt()}));function Ot(e){var t=e.onDragEnd;return[{type:`pointermove`,listener:function(){var e=0;return function(){if(e<20){e++;return}t()}}()},{type:`pointerdown`,listener:t}]}var kt=e((()=>{}));function L(e){return{altKey:e.altKey,button:e.button,buttons:e.buttons,ctrlKey:e.ctrlKey,metaKey:e.metaKey,shiftKey:e.shiftKey,clientX:e.clientX,clientY:e.clientY,pageX:e.pageX,pageY:e.pageY}}var At=e((()=>{})),jt,Mt=e((()=>{jt=function(e){var t=[],n=null,r=function(){t=[...arguments],!n&&(n=requestAnimationFrame(function(){n=null,e.apply(void 0,t)}))};return r.cancel=function(){n&&=(cancelAnimationFrame(n),null)},r}}));function Nt(e){var t=e.source,n=e.initial,r=e.dispatchEvent,i={dropTargets:[]};function a(e){r(e),i={dropTargets:e.payload.location.current.dropTargets}}return{start:function(e){var r=e.nativeSetDragImage,o={current:n,previous:i,initial:n};a({eventName:`onGenerateDragPreview`,payload:{source:t,location:o,nativeSetDragImage:r}}),z.schedule(function(){a({eventName:`onDragStart`,payload:{source:t,location:o}})})},dragUpdate:function(e){var r=e.current;z.flush(),R.cancel(),a({eventName:`onDropTargetChange`,payload:{source:t,location:{initial:n,previous:i,current:r}}})},drag:function(e){var r=e.current;R(function(){z.flush(),a({eventName:`onDrag`,payload:{source:t,location:{initial:n,previous:i,current:r}}})})},drop:function(e){var r=e.current,o=e.updatedSourcePayload;z.flush(),R.cancel(),a({eventName:`onDrop`,payload:{source:o??t,location:{current:r,previous:i,initial:n}}})}}}var R,z,Pt=e((()=>{Mt(),R=jt(function(e){return e()}),z=function(){var e=null;function t(t){e={frameId:requestAnimationFrame(function(){e=null,t()}),fn:t}}function n(){e&&=(cancelAnimationFrame(e.frameId),e.fn(),null)}return{schedule:t,flush:n}}()}));function Ft(){return!V.isActive}function It(e){return e.dataTransfer?e.dataTransfer.setDragImage.bind(e.dataTransfer):null}function Lt(e){var t=e.current,n=e.next;if(t.length!==n.length)return!0;for(var r=0;r<t.length;r++)if(t[r].element!==n[r].element)return!0;return!1}function Rt(e){var t=e.event,n=e.dragType,r=e.getDropTargetsOver,i=e.dispatchEvent;if(!Ft())return;var a=zt({event:t,dragType:n,getDropTargetsOver:r});V.isActive=!0;var o={current:a};B({event:t,current:a.dropTargets});var s=Nt({source:n.payload,dispatchEvent:i,initial:a});function c(e){var t=Lt({current:o.current.dropTargets,next:e.dropTargets});o.current=e,t&&s.dragUpdate({current:o.current})}function l(e){var t=L(e),i=r({target:He(e.target)?We({x:t.clientX,y:t.clientY}):e.target,input:t,source:n.payload,current:o.current.dropTargets});i.length&&(e.preventDefault(),B({event:e,current:i})),c({dropTargets:i,input:t})}function u(){o.current.dropTargets.length&&c({dropTargets:[],input:o.current.input}),s.drop({current:o.current,updatedSourcePayload:null}),d()}function d(){V.isActive=!1,f()}var f=(0,Bt.bindAll)(window,[{type:`dragover`,listener:function(e){l(e),s.drag({current:o.current})}},{type:`dragenter`,listener:l},{type:`dragleave`,listener:function(e){Et({dragLeave:e})&&(c({input:o.current.input,dropTargets:[]}),n.startedFrom===`external`&&u())}},{type:`drop`,listener:function(e){if(o.current={dropTargets:o.current.dropTargets,input:L(e)},!o.current.dropTargets.length){u();return}e.preventDefault(),B({event:e,current:o.current.dropTargets}),s.drop({current:o.current,updatedSourcePayload:n.type===`external`?n.getDropPayload(e):null}),d()}},{type:`dragend`,listener:function(e){o.current={dropTargets:o.current.dropTargets,input:L(e)},u()}}].concat(ht(Ot({onDragEnd:u}))),{capture:!0});s.start({nativeSetDragImage:It(t)})}function B(e){var t=e.event,n=e.current[0]?.dropEffect;n!=null&&t.dataTransfer&&(t.dataTransfer.dropEffect=n)}function zt(e){var t=e.event,n=e.dragType,r=e.getDropTargetsOver,i=L(t);return n.startedFrom===`external`?{input:i,dropTargets:[]}:{input:i,dropTargets:r({input:i,source:n.payload,target:t.target,current:[]})}}var Bt,V,H,Vt=e((()=>{gt(),Bt=O(),Ge(),Ue(),Dt(),kt(),At(),Pt(),V={isActive:!1},H={canStart:Ft,start:Rt}}));function Ht(e){var t=e.typeKey,n=e.mount,r=U.get(t);if(r)return r.usageCount++,r;var i={typeKey:t,unmount:n(),usageCount:1};return U.set(t,i),i}function Ut(e){var t=Ht(e);return function(){t.usageCount--,!(t.usageCount>0)&&(t.unmount(),U.delete(e.typeKey))}}var U,Wt=e((()=>{U=new Map}));function Gt(){var e=[...arguments];return function(){e.forEach(function(e){return e()})}}var Kt=e((()=>{}));function qt(e,t){var n=t.attribute,r=t.value;return e.setAttribute(n,r),function(){return e.removeAttribute(n)}}var Jt=e((()=>{}));function Yt(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function W(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?Yt(Object(n),!0).forEach(function(t){x(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):Yt(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function Xt(e,t){var n=typeof Symbol<`u`&&e[Symbol.iterator]||e[`@@iterator`];if(!n){if(Array.isArray(e)||(n=Zt(e))||t&&e&&typeof e.length==`number`){n&&(e=n);var r=0,i=function(){};return{s:i,n:function(){return r>=e.length?{done:!0}:{done:!1,value:e[r++]}},e:function(e){throw e},f:i}}throw TypeError(`Invalid attempt to iterate non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var a,o=!0,s=!1;return{s:function(){n=n.call(e)},n:function(){var e=n.next();return o=e.done,e},e:function(e){s=!0,a=e},f:function(){try{o||n.return==null||n.return()}finally{if(s)throw a}}}}function Zt(e,t){if(e){if(typeof e==`string`)return Qt(e,t);var n={}.toString.call(e).slice(8,-1);return n===`Object`&&e.constructor&&(n=e.constructor.name),n===`Map`||n===`Set`?Array.from(e):n===`Arguments`||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?Qt(e,t):void 0}}function Qt(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}function $t(e){return e.slice(0).reverse()}function en(e){var t=e.typeKey,n=e.defaultDropEffect,r=new WeakMap,i=`data-drop-target-for-${t}`,a=`[${i}]`;function o(e){return r.set(e.element,e),function(){return r.delete(e.element)}}function s(e){return k(Gt(qt(e.element,{attribute:i,value:`true`}),o(e)))}function c(e){var t=e.source,i=e.target,o=e.input,s=e.result,l=s===void 0?[]:s;if(i==null)return l;if(!(i instanceof Element))return i instanceof Node?c({source:t,target:i.parentElement,input:o,result:l}):l;var u=i.closest(a);if(u==null)return l;var d=r.get(u);if(d==null)return l;var f={input:o,source:t,element:d.element};if(d.canDrop&&!d.canDrop(f))return c({source:t,target:d.element.parentElement,input:o,result:l});var p=d.getData?.call(d,f)??{},m=d.getDropEffect?.call(d,f)??n,h={data:p,element:d.element,dropEffect:m,isActiveDueToStickiness:!1};return c({source:t,target:d.element.parentElement,input:o,result:[].concat(ht(l),[h])})}function l(e){var t=e.eventName,n=e.payload,i=Xt(n.location.current.dropTargets),a;try{for(i.s();!(a=i.n()).done;){var o,s=a.value,c=r.get(s.element),l=W(W({},n),{},{self:s});c==null||(o=c[t])==null||o.call(c,l)}}catch(e){i.e(e)}finally{i.f()}}var u={onGenerateDragPreview:l,onDrag:l,onDragStart:l,onDrop:l,onDropTargetChange:function(e){var t=e.payload,n=new Set(t.location.current.dropTargets.map(function(e){return e.element})),i=new Set,a=Xt(t.location.previous.dropTargets),o;try{for(a.s();!(o=a.n()).done;){var s,c=o.value;i.add(c.element);var l=r.get(c.element),u=n.has(c.element),d=W(W({},t),{},{self:c});if(l==null||(s=l.onDropTargetChange)==null||s.call(l,d),!u){var f;l==null||(f=l.onDragLeave)==null||f.call(l,d)}}}catch(e){a.e(e)}finally{a.f()}var p=Xt(t.location.current.dropTargets),m;try{for(p.s();!(m=p.n()).done;){var h,g,_=m.value;if(!i.has(_.element)){var v=W(W({},t),{},{self:_}),y=r.get(_.element);y==null||(h=y.onDropTargetChange)==null||h.call(y,v),y==null||(g=y.onDragEnter)==null||g.call(y,v)}}}catch(e){p.e(e)}finally{p.f()}}};function d(e){u[e.eventName](e)}function f(e){var t=e.source,n=e.target,i=e.input,a=e.current,o=c({source:t,target:n,input:i});if(o.length>=a.length)return o;for(var s=$t(a),l=$t(o),u=[],d=0;d<s.length;d++){var f,p=s[d],m=l[d];if(m!=null){u.push(m);continue}var h=u[d-1],g=s[d-1];if(h?.element!==g?.element)break;var _=r.get(p.element);if(!_)break;var v={input:i,source:t,element:_.element};if(_.canDrop&&!_.canDrop(v)||!((f=_.getIsSticky)!=null&&f.call(_,v)))break;u.push(W(W({},p),{},{isActiveDueToStickiness:!0}))}return $t(u)}return{dropTargetForConsumers:s,getIsOver:f,dispatchEvent:d}}var tn=e((()=>{S(),gt(),Kt(),A(),Jt()}));function nn(e,t){var n=typeof Symbol<`u`&&e[Symbol.iterator]||e[`@@iterator`];if(!n){if(Array.isArray(e)||(n=rn(e))||t&&e&&typeof e.length==`number`){n&&(e=n);var r=0,i=function(){};return{s:i,n:function(){return r>=e.length?{done:!0}:{done:!1,value:e[r++]}},e:function(e){throw e},f:i}}throw TypeError(`Invalid attempt to iterate non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var a,o=!0,s=!1;return{s:function(){n=n.call(e)},n:function(){var e=n.next();return o=e.done,e},e:function(e){s=!0,a=e},f:function(){try{o||n.return==null||n.return()}finally{if(s)throw a}}}}function rn(e,t){if(e){if(typeof e==`string`)return an(e,t);var n={}.toString.call(e).slice(8,-1);return n===`Object`&&e.constructor&&(n=e.constructor.name),n===`Map`||n===`Set`?Array.from(e):n===`Arguments`||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?an(e,t):void 0}}function an(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}function on(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function sn(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?on(Object(n),!0).forEach(function(t){x(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):on(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function cn(){var e=new Set,t=null;function n(e){t&&(!e.canMonitor||e.canMonitor(t.canMonitorArgs))&&t.active.add(e)}function r(r){var i=sn({},r);e.add(i),n(i);function a(){e.delete(i),t&&t.active.delete(i)}return k(a)}function i(r){var i=r.eventName,a=r.payload;if(i===`onGenerateDragPreview`){t={canMonitorArgs:{initial:a.location.initial,source:a.source},active:new Set};var o=nn(e),s;try{for(o.s();!(s=o.n()).done;){var c=s.value;n(c)}}catch(e){o.e(e)}finally{o.f()}}if(t){for(var l=Array.from(t.active),u=0,d=l;u<d.length;u++){var f=d[u];if(t.active.has(f)){var p;(p=f[i])==null||p.call(f,a)}}i===`onDrop`&&(t.active.clear(),t=null)}}return{dispatchEvent:i,monitorForConsumers:r}}var ln=e((()=>{S(),A()}));function un(e){var t=e.typeKey,n=e.mount,r=e.dispatchEventToSource,i=e.onPostDispatch,a=e.defaultDropEffect,o=cn(),s=en({typeKey:t,defaultDropEffect:a});function c(e){r?.(e),s.dispatchEvent(e),o.dispatchEvent(e),i?.(e)}function l(e){var t=e.event,n=e.dragType;H.start({event:t,dragType:n,getDropTargetsOver:s.getIsOver,dispatchEvent:c})}function u(){function e(){return n({canStart:H.canStart,start:l})}return Ut({typeKey:t,mount:e})}return{registerUsage:u,dropTarget:s.dropTargetForConsumers,monitor:o.monitorForConsumers}}var dn=e((()=>{Vt(),Wt(),tn(),ln()})),fn,pn,mn=e((()=>{A(),fn=k(function(){return navigator.userAgent.toLocaleLowerCase().includes(`android`)}),pn=`pdnd:android-fallback`})),hn,gn=e((()=>{hn=`text/plain`})),_n=e((()=>{})),vn,yn=e((()=>{vn=`application/vnd.pdnd`}));function bn(e){return G.set(e.element,e),function(){G.delete(e.element)}}function xn(e){return k(Gt(K.registerUsage(),bn(e),qt(e.element,{attribute:`draggable`,value:`true`})))}var Sn,G,Cn,K,wn,Tn,En=e((()=>{D(),Sn=O(),Ge(),ct(),dn(),Kt(),A(),Jt(),mn(),At(),gn(),_n(),yn(),G=new WeakMap,Cn=st(),K=un({typeKey:`element`,defaultDropEffect:`move`,mount:function(e){return Gt(Cn.bindEvents(),(0,Sn.bind)(document,{type:`dragstart`,listener:function(t){if(e.canStart(t)&&!t.defaultPrevented&&t.dataTransfer){var n=t.target;if(n instanceof HTMLElement){var r=G.get(n);if(r){var i=L(t),a={element:r.element,dragHandle:r.dragHandle??null,input:i};if(r.canDrag&&!r.canDrag(a)){t.preventDefault();return}if(r.dragHandle){var o=We({x:i.clientX,y:i.clientY});if(!r.dragHandle.contains(o)){t.preventDefault();return}}var s=r.getInitialDataForExternal?.call(r,a)??null;if(s)for(var c=0,l=Object.entries(s);c<l.length;c++){var u=Le(l[c],2),d=u[0],f=u[1];t.dataTransfer.setData(d,f??``)}fn()&&!t.dataTransfer.types.includes(`text/plain`)&&!t.dataTransfer.types.includes(`text/uri-list`)&&t.dataTransfer.setData(hn,pn),t.dataTransfer.setData(vn,``);var p={type:`element`,payload:{element:r.element,dragHandle:r.dragHandle??null,data:r.getInitialData?.call(r,a)??{}},startedFrom:`internal`};e.start({event:t,dragType:p})}}}}}))},dispatchEventToSource:function(e){var t,n,r=e.eventName,i=e.payload;(t=G.get(i.source.element))==null||(n=t[r])==null||n.call(t,i)},onPostDispatch:Cn.getOnPostDispatch()}),wn=K.dropTarget,Tn=K.monitor})),Dn=e((()=>{En()}));function On(e){var t=e.list,n=e.startIndex,r=e.finishIndex;if(n===-1||r===-1)return Array.from(t);var i=Array.from(t),a=Le(i.splice(n,1),1)[0];return i.splice(r,0,a),i}var kn=e((()=>{D()})),An=e((()=>{kn()}));function q(e){let t=h(!1),n=e.enabled??h(!0);return m([e.element,()=>e.dragHandle?.value,n],([n,r,i],a,o)=>{!n||!i||o(xn({element:n,dragHandle:r??void 0,canDrag:e.canDrag,getInitialData:e.getInitialData,onDragStart:()=>{t.value=!0},onDrop:()=>{t.value=!1}}))},{flush:`post`,immediate:!0}),{isDragging:t}}var jn,Mn=e((()=>{Dn(),i(),jn=`csp-sortable-item`,q.__docgenInfo=Object.assign({displayName:q.name??q.__name},{exportName:`useDraggableElement`,displayName:`useDraggableElement`,type:2,props:[{name:`element`,global:!1,description:``,tags:[],required:!0,type:`Ref<HTMLElement, HTMLElement>`,declarations:[],schema:`Ref<HTMLElement, HTMLElement>`},{name:`dragHandle`,global:!1,description:``,tags:[],required:!1,type:`Ref<HTMLElement, HTMLElement>`,declarations:[],schema:`Ref<HTMLElement, HTMLElement>`},{name:`enabled`,global:!1,description:``,tags:[],required:!1,type:`Ref<boolean, boolean>`,declarations:[],schema:`Ref<boolean, boolean>`},{name:`canDrag`,global:!1,description:``,tags:[],required:!1,type:`() => boolean`,declarations:[],schema:{kind:`event`,type:`(): boolean`}},{name:`getInitialData`,global:!1,description:``,tags:[],required:!0,type:`() => Record<string, unknown>`,declarations:[],schema:{kind:`event`,type:`(): Record<string, unknown>`}}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/composables/dnd/useDraggableElement.ts`})}));function J(e){let t=h(!1),n=h(null),r=e.enabled??h(!0);return m([e.element,r],([r,i],a,o)=>{!r||!i||o(wn({element:r,canDrop:({source:t})=>!(e.canDrop&&!e.canDrop(t.data)),getData:({input:t,element:n})=>pe(e.getData({input:t,element:n}),{input:t,element:n,allowedEdges:[`top`,`bottom`]}),onDragEnter:({self:e})=>{t.value=!0,n.value=me(e.data)},onDrag:({self:e})=>{n.value=me(e.data)},onDragLeave:()=>{t.value=!1,n.value=null},onDrop:()=>{t.value=!1,n.value=null}}))},{flush:`post`,immediate:!0}),{isDraggedOver:t,closestEdge:n}}var Nn=e((()=>{ge(),Dn(),i(),J.__docgenInfo=Object.assign({displayName:J.name??J.__name},{exportName:`useDropTargetElement`,displayName:`useDropTargetElement`,type:2,props:[{name:`element`,global:!1,description:``,tags:[],required:!0,type:`Ref<HTMLElement, HTMLElement>`,declarations:[],schema:`Ref<HTMLElement, HTMLElement>`},{name:`enabled`,global:!1,description:``,tags:[],required:!1,type:`Ref<boolean, boolean>`,declarations:[],schema:`Ref<boolean, boolean>`},{name:`canDrop`,global:!1,description:``,tags:[],required:!1,type:`(source: Record<string, unknown>) => boolean`,declarations:[],schema:{kind:`event`,type:`(source: Record<string, unknown>): boolean`}},{name:`getData`,global:!1,description:``,tags:[],required:!0,type:`(args: { input: Input; element: Element; }) => Record<string, unknown>`,declarations:[],schema:{kind:`event`,type:`(args: { input: Input; element: Element; }): Record<string, unknown>`}}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/composables/dnd/useDropTargetElement.ts`})})),Pn,Fn,Y,In=e((()=>{i(),Mn(),Nn(),Pn={key:0,class:`csp-sortable-list-item__indicator csp-sortable-list-item__indicator--top`},Fn={key:1,class:`csp-sortable-list-item__indicator csp-sortable-list-item__indicator--bottom`},Y=o({__name:`CspSortableListItem`,props:{item:{},itemId:{},index:{},listId:{},draggable:{type:Boolean,default:!0},disabled:{type:Boolean,default:!1}},setup(e){let t=e,n=h(null),r=h(null),i=l(()=>!t.disabled),a=l(()=>t.draggable&&i.value);function o(){return{type:jn,listId:t.listId,itemId:t.itemId,index:t.index}}let{isDragging:p}=q({element:n,dragHandle:r,enabled:a,getInitialData:o}),{isDraggedOver:m,closestEdge:g}=J({element:n,enabled:i,canDrop:e=>e.type===`csp-sortable-item`&&e.listId===t.listId,getData:()=>o()});function _(e){r.value=e}return(r,i)=>(d(),s(`li`,{ref_key:`itemRef`,ref:n,class:y([`csp-sortable-list-item`,{"csp-sortable-list-item--dragging":c(p),"csp-sortable-list-item--drag-over":c(m)}])},[c(m)&&c(g)===`top`?(d(),s(`div`,Pn)):u(``,!0),f(r.$slots,`default`,{item:e.item,index:t.index,isDragging:c(p),isDraggedOver:c(m),closestEdge:c(g),setHandleRef:_,isDraggable:a.value},void 0,!0),c(m)&&c(g)===`bottom`?(d(),s(`div`,Fn)):u(``,!0)],2))}})})),Ln=e((()=>{})),Rn,zn=e((()=>{In(),In(),Ln(),ee(),Rn=te(Y,[[`__scopeId`,`data-v-15907b04`]]),Y.__docgenInfo=Object.assign({displayName:Y.name??Y.__name},{exportName:`default`,displayName:`CspSortableListItem`,type:2,props:[{name:`item`,global:!1,description:``,tags:[],required:!0,type:`unknown`,declarations:[],schema:`unknown`},{name:`itemId`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`index`,global:!1,description:``,tags:[],required:!0,type:`number`,declarations:[],schema:`number`},{name:`listId`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`draggable`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`disabled`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`default`,type:`{ item: unknown; index: number; isDragging: any; isDraggedOver: any; closestEdge: any; setHandleRef: (element: Element) => void; isDraggable: boolean; }`,description:``,declarations:[],schema:{kind:`object`,type:`{ item: unknown; index: number; isDragging: any; isDraggedOver: any; closestEdge: any; setHandleRef: (element: Element) => void; isDraggable: boolean; }`}}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspSortableList/CspSortableListItem.vue`})})),Bn,X,Vn=e((()=>{i(),ge(),ve(),Ee(),Dn(),An(),Mn(),zn(),Bn={class:`csp-sortable-list`},X=o({__name:`CspSortableList`,props:{items:{},getItemKey:{},getItemLabel:{},isItemDraggable:{},disabled:{type:Boolean,default:!1}},emits:[`reorder`],setup(e,{emit:t}){let i=e,o=t,l=p();function u(e,t){return i.disabled?!1:i.isItemDraggable?.(e,t)??!0}function m(e){return i.getItemLabel?.(e)??i.getItemKey(e)}function h(e,t){if(i.disabled||t<0||t>=i.items.length||!u(i.items[e],e))return;o(`reorder`,On({list:i.items,startIndex:e,finishIndex:t}));let n=i.items[e];we(`${m(n)} déplacé`)}function y(e){return()=>h(e,e-1)}function ee(e){return()=>h(e,e+1)}return g(()=>Tn({canMonitor:({source:e})=>e.data.type===`csp-sortable-item`&&e.data.listId===l,onDrop:({source:e,location:t})=>{if(i.disabled)return;let n=t.current.dropTargets[0];if(!n)return;let r=e.data.index,a=n.data.index;if(typeof r!=`number`||typeof a!=`number`)return;let s=_e({startIndex:r,indexOfTarget:a,closestEdgeOfTarget:me(n.data),axis:`vertical`});if(s===r)return;o(`reorder`,On({list:i.items,startIndex:r,finishIndex:s}));let c=i.items[r];we(`${m(c)} déplacé`)}})),(t,i)=>(d(),s(`ul`,Bn,[(d(!0),s(a,null,_(e.items,(i,a)=>(d(),r(Rn,{key:e.getItemKey(i),item:i,"item-id":e.getItemKey(i),index:a,"list-id":c(l),draggable:u(i,a),disabled:e.disabled},{default:v(r=>[f(t.$slots,`item`,n({ref_for:!0},r,{canMoveUp:u(i,a)&&a>0,canMoveDown:u(i,a)&&a<e.items.length-1,moveUp:y(a),moveDown:ee(a)}),void 0,!0)]),_:2},1032,[`item`,`item-id`,`index`,`list-id`,`draggable`,`disabled`]))),128))]))}})})),Hn=e((()=>{})),Z,Un=e((()=>{Vn(),Vn(),Hn(),ee(),Z=te(X,[[`__scopeId`,`data-v-d842298b`]]),X.__docgenInfo=Object.assign({displayName:X.name??X.__name},{exportName:`default`,displayName:`CspSortableList`,type:2,props:[{name:`items`,global:!1,description:``,tags:[],required:!0,type:`unknown[]`,declarations:[],schema:{kind:`array`,type:`unknown[]`}},{name:`getItemKey`,global:!1,description:``,tags:[],required:!0,type:`(item: unknown) => string`,declarations:[],schema:{kind:`event`,type:`(item: unknown): string`}},{name:`getItemLabel`,global:!1,description:``,tags:[],required:!1,type:`(item: unknown) => string`,declarations:[],schema:{kind:`event`,type:`(item: unknown): string`}},{name:`isItemDraggable`,global:!1,description:``,tags:[],required:!1,type:`(item: unknown, index: number) => boolean`,declarations:[],schema:{kind:`event`,type:`(item: unknown, index: number): boolean`}},{name:`disabled`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`reorder`,description:``,tags:[],type:`[items: unknown[]]`,signature:`(evt: "reorder", items: unknown[]): void`,declarations:[],schema:[{kind:`array`,type:`unknown[]`}]}],slots:[{name:`item`,type:`{ canMoveUp: boolean; canMoveDown: boolean; moveUp: () => void; moveDown: () => void; item: unknown; index: number; isDragging: any; isDraggedOver: any; closestEdge: any; setHandleRef: (element: Element) => void; isDraggable: boolean; }`,description:``,declarations:[],schema:{kind:`object`,type:`{ canMoveUp: boolean; canMoveDown: boolean; moveUp: () => void; moveDown: () => void; item: unknown; index: number; isDragging: any; isDraggedOver: any; closestEdge: any; setHandleRef: (element: Element) => void; isDraggable: boolean; }`}}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspSortableList/CspSortableList.vue`})})),Wn,Gn,Kn,qn,Q,Jn,$,Yn;e((()=>{i(),ie(),ne(),Un(),Wn={title:`Éléments/Génériques/CspSortableList`,component:Z,tags:[`autodocs`],parameters:{controls:{include:[`showAccessibilityButtons`]}},argTypes:{showAccessibilityButtons:{control:{type:`boolean`},description:`Afficher les boutons monter/descendre (accessibilité).`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}}},args:{showAccessibilityButtons:!0}},Gn={display:`flex`,alignItems:`center`,gap:`var(--csp-space-3)`,padding:`var(--csp-space-3) var(--csp-space-4)`,borderRadius:`0.25rem`,boxShadow:`inset 0 0 0 1px var(--border-default-grey)`,background:`var(--background-default-grey)`},Kn={display:`flex`,cursor:`grab`,color:`var(--text-mention-grey)`},qn={display:`flex`,gap:`var(--csp-space-1)`,minWidth:`4rem`},Q={render:e=>({components:{CspSortableList:Z,CspIcon:re,CspButton:ae},setup(){let t=h([{id:`1`,label:`Pré-qualification`},{id:`2`,label:`Entretien téléphonique`},{id:`3`,label:`Entretien technique`},{id:`4`,label:`Entretien RH`}]);function n(e){t.value=e}return{args:e,items:t,itemStyle:Gn,handleStyle:Kn,actionsStyle:qn,getItemKey:e=>e.id,getItemLabel:e=>e.label,onReorder:n}},template:`
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        @reorder="onReorder"
      >
        <template #item="{ item, setHandleRef, isDragging, canMoveUp, canMoveDown, moveUp, moveDown }">
          <div :style="{ ...itemStyle, opacity: isDragging ? 0.5 : 1 }">
            <span :ref="setHandleRef" :style="handleStyle">
              <CspIcon name="ri:drag-drop-line" :size="16" />
            </span>
            <span style="flex: 1;">{{ item.label }}</span>
            <div :style="actionsStyle">
              <template v-if="args.showAccessibilityButtons">
                <CspButton
                  icon="ri:arrow-up-s-line"
                  variant="tertiary-no-outline"
                  size="sm"
                  :disabled="!canMoveUp"
                  aria-label="Monter"
                  @click="moveUp"
                />
                <CspButton
                  icon="ri:arrow-down-s-line"
                  variant="tertiary-no-outline"
                  size="sm"
                  :disabled="!canMoveDown"
                  aria-label="Descendre"
                  @click="moveDown"
                />
              </template>
            </div>
          </div>
        </template>
      </CspSortableList>
    `})},Jn={display:`flex`,color:`var(--text-mention-grey)`},$={args:{showAccessibilityButtons:!0},render:e=>({components:{CspSortableList:Z,CspIcon:re,CspButton:ae},setup(){let t=h([{id:`1`,label:`Candidature reçue`,locked:!0},{id:`2`,label:`Pré-qualification`},{id:`3`,label:`Entretien`},{id:`4`,label:`Entretien RH`},{id:`5`,label:`Offre clôturée`,locked:!0}]);function n(e){t.value=e}return{args:e,items:t,itemStyle:Gn,iconStyle:Jn,actionsStyle:qn,getItemKey:e=>e.id,getItemLabel:e=>e.label,isItemDraggable:e=>!e.locked,onReorder:n}},template:`
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        :is-item-draggable="isItemDraggable"
        @reorder="onReorder"
      >
        <template #item="{ item, setHandleRef, isDragging, isDraggable, canMoveUp, canMoveDown, moveUp, moveDown }">
          <div :style="{ ...itemStyle, opacity: isDragging ? 0.5 : 1 }">
            <span
              v-if="isDraggable"
              :ref="setHandleRef"
              :style="{ ...iconStyle, cursor: 'grab' }"
            >
              <CspIcon name="ri:drag-drop-line" :size="16" />
            </span>
            <span style="flex: 1;">{{ item.label }}</span>
            <div :style="actionsStyle">
              <template v-if="isDraggable && args.showAccessibilityButtons">
                <CspButton
                  icon="ri:arrow-up-s-line"
                  variant="tertiary-no-outline"
                  size="sm"
                  :disabled="!canMoveUp"
                  aria-label="Monter"
                  @click="moveUp"
                />
                <CspButton
                  icon="ri:arrow-down-s-line"
                  variant="tertiary-no-outline"
                  size="sm"
                  :disabled="!canMoveDown"
                  aria-label="Descendre"
                  @click="moveDown"
                />
              </template>
            </div>
          </div>
        </template>
      </CspSortableList>
    `})},Q.parameters={...Q.parameters,docs:{...Q.parameters?.docs,source:{originalSource:`{
  render: (args: StoryArgs) => ({
    components: {
      CspSortableList,
      CspIcon,
      CspButton
    },
    setup() {
      const items = ref<DemoItem[]>([{
        id: '1',
        label: 'Pré-qualification'
      }, {
        id: '2',
        label: 'Entretien téléphonique'
      }, {
        id: '3',
        label: 'Entretien technique'
      }, {
        id: '4',
        label: 'Entretien RH'
      }]);
      function onReorder(newItems: DemoItem[]) {
        items.value = newItems;
      }
      return {
        args,
        items,
        itemStyle,
        handleStyle,
        actionsStyle,
        getItemKey: (item: DemoItem) => item.id,
        getItemLabel: (item: DemoItem) => item.label,
        onReorder
      };
    },
    template: \`
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        @reorder="onReorder"
      >
        <template #item="{ item, setHandleRef, isDragging, canMoveUp, canMoveDown, moveUp, moveDown }">
          <div :style="{ ...itemStyle, opacity: isDragging ? 0.5 : 1 }">
            <span :ref="setHandleRef" :style="handleStyle">
              <CspIcon name="ri:drag-drop-line" :size="16" />
            </span>
            <span style="flex: 1;">{{ item.label }}</span>
            <div :style="actionsStyle">
              <template v-if="args.showAccessibilityButtons">
                <CspButton
                  icon="ri:arrow-up-s-line"
                  variant="tertiary-no-outline"
                  size="sm"
                  :disabled="!canMoveUp"
                  aria-label="Monter"
                  @click="moveUp"
                />
                <CspButton
                  icon="ri:arrow-down-s-line"
                  variant="tertiary-no-outline"
                  size="sm"
                  :disabled="!canMoveDown"
                  aria-label="Descendre"
                  @click="moveDown"
                />
              </template>
            </div>
          </div>
        </template>
      </CspSortableList>
    \`
  })
}`,...Q.parameters?.docs?.source}}},$.parameters={...$.parameters,docs:{...$.parameters?.docs,source:{originalSource:`{
  args: {
    showAccessibilityButtons: true
  },
  render: (args: StoryArgs) => ({
    components: {
      CspSortableList,
      CspIcon,
      CspButton
    },
    setup() {
      const items = ref<LockedDemoItem[]>([{
        id: '1',
        label: 'Candidature reçue',
        locked: true
      }, {
        id: '2',
        label: 'Pré-qualification'
      }, {
        id: '3',
        label: 'Entretien'
      }, {
        id: '4',
        label: 'Entretien RH'
      }, {
        id: '5',
        label: 'Offre clôturée',
        locked: true
      }]);
      function onReorder(newItems: LockedDemoItem[]) {
        items.value = newItems;
      }
      return {
        args,
        items,
        itemStyle,
        iconStyle,
        actionsStyle,
        getItemKey: (item: LockedDemoItem) => item.id,
        getItemLabel: (item: LockedDemoItem) => item.label,
        isItemDraggable: (item: LockedDemoItem) => !item.locked,
        onReorder
      };
    },
    template: \`
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        :is-item-draggable="isItemDraggable"
        @reorder="onReorder"
      >
        <template #item="{ item, setHandleRef, isDragging, isDraggable, canMoveUp, canMoveDown, moveUp, moveDown }">
          <div :style="{ ...itemStyle, opacity: isDragging ? 0.5 : 1 }">
            <span
              v-if="isDraggable"
              :ref="setHandleRef"
              :style="{ ...iconStyle, cursor: 'grab' }"
            >
              <CspIcon name="ri:drag-drop-line" :size="16" />
            </span>
            <span style="flex: 1;">{{ item.label }}</span>
            <div :style="actionsStyle">
              <template v-if="isDraggable && args.showAccessibilityButtons">
                <CspButton
                  icon="ri:arrow-up-s-line"
                  variant="tertiary-no-outline"
                  size="sm"
                  :disabled="!canMoveUp"
                  aria-label="Monter"
                  @click="moveUp"
                />
                <CspButton
                  icon="ri:arrow-down-s-line"
                  variant="tertiary-no-outline"
                  size="sm"
                  :disabled="!canMoveDown"
                  aria-label="Descendre"
                  @click="moveDown"
                />
              </template>
            </div>
          </div>
        </template>
      </CspSortableList>
    \`
  })
}`,...$.parameters?.docs?.source}}},Yn=[`Default`,`WithLockedItems`]}))();export{Q as Default,$ as WithLockedItems,Yn as __namedExportsOrder,Wn as default};