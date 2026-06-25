import{i as e,r as t}from"./preload-helper-DVWsqyFp.js";import{At as n,B as r,Bt as i,D as a,F as o,H as s,K as c,Lt as l,R as u,V as d,ct as f,et as p,gt as m,lt as h,ot as g,pt as _,rt as v,yt as y}from"./iframe-Cn59cvaW.js";import{n as ee,t as te}from"./_plugin-vue_export-helper-BuTp77SO.js";import{n as ne,t as b}from"./CspIcon-CCFxhMkM.js";import{n as re,t as ie}from"./CspButton-BZBJu27A.js";import{n as ae,t as oe}from"./CspDropdownMenu-BojuqPGX.js";function x(e){"@babel/helpers - typeof";return x=typeof Symbol==`function`&&typeof Symbol.iterator==`symbol`?function(e){return typeof e}:function(e){return e&&typeof Symbol==`function`&&e.constructor===Symbol&&e!==Symbol.prototype?`symbol`:typeof e},x(e)}var se=e((()=>{}));function ce(e,t){if(x(e)!=`object`||!e)return e;var n=e[Symbol.toPrimitive];if(n!==void 0){var r=n.call(e,t||`default`);if(x(r)!=`object`)return r;throw TypeError(`@@toPrimitive must return a primitive value.`)}return(t===`string`?String:Number)(e)}var le=e((()=>{se()}));function ue(e){var t=ce(e,`string`);return x(t)==`symbol`?t:t+``}var de=e((()=>{se(),le()}));function S(e,t,n){return(t=ue(t))in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}var C=e((()=>{de()}));function fe(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function pe(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?fe(Object(n),!0).forEach(function(t){S(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):fe(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function me(e,t){var n=t.element,r=t.input,i=t.allowedEdges,a={x:r.clientX,y:r.clientY},o=n.getBoundingClientRect(),s=i.map(function(e){return{edge:e,value:he[e](o,a)}}).sort(function(e,t){return e.value-t.value})[0]?.edge??null;return pe(pe({},e),{},S({},ge,s))}function w(e){return e[ge]??null}var he,ge,_e=e((()=>{C(),he={top:function(e,t){return Math.abs(t.y-e.top)},right:function(e,t){return Math.abs(e.right-t.x)},bottom:function(e,t){return Math.abs(e.bottom-t.y)},left:function(e,t){return Math.abs(t.x-e.left)}},ge=Symbol(`closestEdge`)}));function ve(e){var t=e.startIndex,n=e.closestEdgeOfTarget,r=e.indexOfTarget,i=e.axis;if(t===-1||r===-1||t===r)return t;if(n==null)return r;var a=i===`vertical`&&n===`bottom`||i===`horizontal`&&n===`right`;return t<r?a?r:r-1:a?r+1:r}var ye=e((()=>{})),be,xe=e((()=>{be=1e3}));function Se(){var e=document.createElement(`div`);return e.setAttribute(`role`,`status`),Object.assign(e.style,Ee),document.body.append(e),e}function Ce(){return T===null&&(T=Se()),T}function we(){D!==null&&clearTimeout(D),D=null}function Te(e){Ce(),we(),D=setTimeout(function(){D=null;var t=Ce();t.textContent=e},be)}var T,E,Ee,D,De=e((()=>{xe(),T=null,E=`1px`,Ee={width:E,height:E,padding:`0`,position:`absolute`,border:`0`,clip:`rect(${E}, ${E}, ${E}, ${E})`,overflow:`hidden`,whiteSpace:`nowrap`,marginTop:`-${E}`,pointerEvents:`none`},D=null}));function Oe(e){if(Array.isArray(e))return e}var ke=e((()=>{}));function Ae(e,t){var n=e==null?null:typeof Symbol<`u`&&e[Symbol.iterator]||e[`@@iterator`];if(n!=null){var r,i,a,o,s=[],c=!0,l=!1;try{if(a=(n=n.call(e)).next,t===0){if(Object(n)!==n)return;c=!1}else for(;!(c=(r=a.call(n)).done)&&(s.push(r.value),s.length!==t);c=!0);}catch(e){l=!0,i=e}finally{try{if(!c&&n.return!=null&&(o=n.return(),Object(o)!==o))return}finally{if(l)throw i}}return s}}var je=e((()=>{}));function Me(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}var Ne=e((()=>{}));function Pe(e,t){if(e){if(typeof e==`string`)return Me(e,t);var n={}.toString.call(e).slice(8,-1);return n===`Object`&&e.constructor&&(n=e.constructor.name),n===`Map`||n===`Set`?Array.from(e):n===`Arguments`||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?Me(e,t):void 0}}var Fe=e((()=>{Ne()}));function Ie(){throw TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var Le=e((()=>{}));function Re(e,t){return Oe(e)||Ae(e,t)||Pe(e,t)||Ie()}var ze=e((()=>{ke(),je(),Fe(),Le()})),Be=t((e=>{Object.defineProperty(e,"__esModule",{value:!0}),e.bind=void 0;function t(e,t){var n=t.type,r=t.listener,i=t.options;return e.addEventListener(n,r,i),function(){e.removeEventListener(n,r,i)}}e.bind=t})),Ve=t((e=>{var t=e&&e.__assign||function(){return t=Object.assign||function(e){for(var t,n=1,r=arguments.length;n<r;n++)for(var i in t=arguments[n],t)Object.prototype.hasOwnProperty.call(t,i)&&(e[i]=t[i]);return e},t.apply(this,arguments)};Object.defineProperty(e,"__esModule",{value:!0}),e.bindAll=void 0;var n=Be();function r(e){if(e!==void 0)return typeof e==`boolean`?{capture:e}:e}function i(e,n){return n==null?e:t(t({},e),{options:t(t({},r(n)),r(e.options))})}function a(e,t,r){var a=t.map(function(t){var a=i(t,r);return(0,n.bind)(e,a)});return function(){a.forEach(function(e){return e()})}}e.bindAll=a})),O=t((e=>{Object.defineProperty(e,"__esModule",{value:!0}),e.bindAll=e.bind=void 0;var t=Be();Object.defineProperty(e,"bind",{enumerable:!0,get:function(){return t.bind}});var n=Ve();Object.defineProperty(e,"bindAll",{enumerable:!0,get:function(){return n.bindAll}})})),He,Ue=e((()=>{He=`data-pdnd-honey-pot`}));function We(e){return e instanceof Element&&e.hasAttribute(`data-pdnd-honey-pot`)}var Ge=e((()=>{Ue()}));function Ke(e){var t=Re(document.elementsFromPoint(e.x,e.y),2),n=t[0],r=t[1];return n?We(n)?r??null:n:null}var qe=e((()=>{ze(),Ge()})),Je,Ye=e((()=>{Je=2147483647})),Xe,Ze=e((()=>{Xe={inset:`unset`,border:`none`,padding:0,margin:0,overflow:`visible`,color:`inherit`,background:`transparent`,width:`auto`,height:`auto`}}));function k(e){var t=null;return function(){if(!t){var n=[...arguments];t={result:e.apply(this,n)}}return t.result}}var A=e((()=>{})),j,Qe=e((()=>{A(),j=k(function(){return typeof HTMLElement<`u`&&typeof HTMLElement.prototype.showPopover==`function`})}));function $e(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function et(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?$e(Object(n),!0).forEach(function(t){S(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):$e(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function tt(e){return{x:Math.floor(e.x),y:Math.floor(e.y)}}function nt(e){return{x:e.x-P,y:e.y-P}}function rt(e){return{x:Math.max(e.x,0),y:Math.max(e.y,0)}}function it(e){return{x:Math.min(e.x,window.innerWidth-N),y:Math.min(e.y,window.innerHeight-N)}}function at(e){var t=e.client,n=it(rt(nt(tt(t))));return DOMRect.fromRect({x:n.x,y:n.y,width:N,height:N})}function ot(e){var t=e.clientRect;return{left:`${t.left}px`,top:`${t.top}px`,width:`${t.width}px`,height:`${t.height}px`}}function st(e){var t=e.client,n=e.clientRect;return t.x>=n.x&&t.x<=n.x+n.width&&t.y>=n.y&&t.y<=n.y+n.height}function ct(e){var t=e.initial,n=document.createElement(`div`);n.setAttribute(He,`true`),j()&&n.setAttribute(`popover`,`manual`);var r=at({client:t});Object.assign(n.style,et(et({position:`fixed`},j()?Xe:{zIndex:Je}),{},{backgroundColor:`transparent`,padding:0,margin:0,boxSizing:`border-box`,pointerEvents:`auto`},ot({clientRect:r}))),document.body.appendChild(n),j()&&n.showPopover();var i=(0,M.bind)(window,{type:`pointermove`,listener:function(e){r=at({client:{x:e.clientX,y:e.clientY}}),Object.assign(n.style,ot({clientRect:r}))},options:{capture:!0}});return function(e){var t=e.current;if(i(),st({client:t,clientRect:r})){n.remove();return}function a(){o(),n.remove()}var o=(0,M.bindAll)(window,[{type:`pointerdown`,listener:a},{type:`pointermove`,listener:a},{type:`focusin`,listener:a},{type:`focusout`,listener:a},{type:`dragstart`,listener:a},{type:`dragenter`,listener:a},{type:`dragover`,listener:a}],{capture:!0})}}function lt(){var e=null;function t(){return e=null,(0,M.bind)(window,{type:`pointermove`,listener:function(t){e={x:t.clientX,y:t.clientY}},options:{capture:!0}})}function n(){var t=null;return function(n){var r=n.eventName,i=n.payload;if(r===`onDragStart`){var a=i.location.initial.input;t=ct({initial:e??{x:a.clientX,y:a.clientY}})}if(r===`onDrop`){var o,s=i.location.current.input;(o=t)==null||o({current:{x:s.clientX,y:s.clientY}}),t=null,e=null}}}return{bindEvents:t,getOnPostDispatch:n}}var M,N,P,ut=e((()=>{C(),M=O(),Ye(),Ze(),Qe(),Ue(),N=2,P=N/2}));function dt(e){if(Array.isArray(e))return Me(e)}var ft=e((()=>{Ne()}));function pt(e){if(typeof Symbol<`u`&&e[Symbol.iterator]!=null||e[`@@iterator`]!=null)return Array.from(e)}var mt=e((()=>{}));function ht(){throw TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var gt=e((()=>{}));function _t(e){return dt(e)||pt(e)||Pe(e)||ht()}var vt=e((()=>{ft(),mt(),Fe(),gt()})),yt,bt=e((()=>{A(),yt=k(function(){return navigator.userAgent.includes(`Firefox`)})})),F,xt=e((()=>{A(),F=k(function(){var e=navigator.userAgent;return e.includes(`AppleWebKit`)&&!e.includes(`Chrome`)})}));function St(e){var t=e.dragLeave;return F()?t.hasOwnProperty(I.isLeavingWindow):!1}var Ct,I,wt=e((()=>{Ct=O(),xt(),I={isLeavingWindow:Symbol(`leaving`),isEnteringWindow:Symbol(`entering`)},(function(){if(typeof window>`u`||!F())return;function e(){return{enterCount:0,isOverWindow:!1}}var t=e();function n(){t=e()}(0,Ct.bindAll)(window,[{type:`dragstart`,listener:function(){t.enterCount=0,t.isOverWindow=!0}},{type:`drop`,listener:n},{type:`dragend`,listener:n},{type:`dragenter`,listener:function(e){!t.isOverWindow&&t.enterCount===0&&(e[I.isEnteringWindow]=!0),t.isOverWindow=!0,t.enterCount++}},{type:`dragleave`,listener:function(e){t.enterCount--,t.isOverWindow&&t.enterCount===0&&(e[I.isLeavingWindow]=!0,t.isOverWindow=!1)}}],{capture:!0})})()}));function Tt(e){return`nodeName`in e}function Et(e){return Tt(e)&&e.ownerDocument!==document}var Dt=e((()=>{}));function Ot(e){var t=e.dragLeave,n=t.type,r=t.relatedTarget;return n===`dragleave`?F()?St({dragLeave:t}):r==null?!0:yt()?Et(r):r instanceof HTMLIFrameElement:!1}var kt=e((()=>{bt(),xt(),wt(),Dt()}));function At(e){var t=e.onDragEnd;return[{type:`pointermove`,listener:function(){var e=0;return function(){if(e<20){e++;return}t()}}()},{type:`pointerdown`,listener:t}]}var jt=e((()=>{}));function L(e){return{altKey:e.altKey,button:e.button,buttons:e.buttons,ctrlKey:e.ctrlKey,metaKey:e.metaKey,shiftKey:e.shiftKey,clientX:e.clientX,clientY:e.clientY,pageX:e.pageX,pageY:e.pageY}}var Mt=e((()=>{})),Nt,Pt=e((()=>{Nt=function(e){var t=[],n=null,r=function(){t=[...arguments],!n&&(n=requestAnimationFrame(function(){n=null,e.apply(void 0,t)}))};return r.cancel=function(){n&&=(cancelAnimationFrame(n),null)},r}}));function Ft(e){var t=e.source,n=e.initial,r=e.dispatchEvent,i={dropTargets:[]};function a(e){r(e),i={dropTargets:e.payload.location.current.dropTargets}}return{start:function(e){var r=e.nativeSetDragImage,o={current:n,previous:i,initial:n};a({eventName:`onGenerateDragPreview`,payload:{source:t,location:o,nativeSetDragImage:r}}),z.schedule(function(){a({eventName:`onDragStart`,payload:{source:t,location:o}})})},dragUpdate:function(e){var r=e.current;z.flush(),R.cancel(),a({eventName:`onDropTargetChange`,payload:{source:t,location:{initial:n,previous:i,current:r}}})},drag:function(e){var r=e.current;R(function(){z.flush(),a({eventName:`onDrag`,payload:{source:t,location:{initial:n,previous:i,current:r}}})})},drop:function(e){var r=e.current,o=e.updatedSourcePayload;z.flush(),R.cancel(),a({eventName:`onDrop`,payload:{source:o??t,location:{current:r,previous:i,initial:n}}})}}}var R,z,It=e((()=>{Pt(),R=Nt(function(e){return e()}),z=function(){var e=null;function t(t){e={frameId:requestAnimationFrame(function(){e=null,t()}),fn:t}}function n(){e&&=(cancelAnimationFrame(e.frameId),e.fn(),null)}return{schedule:t,flush:n}}()}));function Lt(){return!B.isActive}function Rt(e){return e.dataTransfer?e.dataTransfer.setDragImage.bind(e.dataTransfer):null}function zt(e){var t=e.current,n=e.next;if(t.length!==n.length)return!0;for(var r=0;r<t.length;r++)if(t[r].element!==n[r].element)return!0;return!1}function Bt(e){var t=e.event,n=e.dragType,r=e.getDropTargetsOver,i=e.dispatchEvent;if(!Lt())return;var a=Ht({event:t,dragType:n,getDropTargetsOver:r});B.isActive=!0;var o={current:a};Vt({event:t,current:a.dropTargets});var s=Ft({source:n.payload,dispatchEvent:i,initial:a});function c(e){var t=zt({current:o.current.dropTargets,next:e.dropTargets});o.current=e,t&&s.dragUpdate({current:o.current})}function l(e){var t=L(e),i=r({target:We(e.target)?Ke({x:t.clientX,y:t.clientY}):e.target,input:t,source:n.payload,current:o.current.dropTargets});i.length&&(e.preventDefault(),Vt({event:e,current:i})),c({dropTargets:i,input:t})}function u(){o.current.dropTargets.length&&c({dropTargets:[],input:o.current.input}),s.drop({current:o.current,updatedSourcePayload:null}),d()}function d(){B.isActive=!1,f()}var f=(0,Ut.bindAll)(window,[{type:`dragover`,listener:function(e){l(e),s.drag({current:o.current})}},{type:`dragenter`,listener:l},{type:`dragleave`,listener:function(e){Ot({dragLeave:e})&&(c({input:o.current.input,dropTargets:[]}),n.startedFrom===`external`&&u())}},{type:`drop`,listener:function(e){if(o.current={dropTargets:o.current.dropTargets,input:L(e)},!o.current.dropTargets.length){u();return}e.preventDefault(),Vt({event:e,current:o.current.dropTargets}),s.drop({current:o.current,updatedSourcePayload:n.type===`external`?n.getDropPayload(e):null}),d()}},{type:`dragend`,listener:function(e){o.current={dropTargets:o.current.dropTargets,input:L(e)},u()}}].concat(_t(At({onDragEnd:u}))),{capture:!0});s.start({nativeSetDragImage:Rt(t)})}function Vt(e){var t=e.event,n=e.current[0]?.dropEffect;n!=null&&t.dataTransfer&&(t.dataTransfer.dropEffect=n)}function Ht(e){var t=e.event,n=e.dragType,r=e.getDropTargetsOver,i=L(t);return n.startedFrom===`external`?{input:i,dropTargets:[]}:{input:i,dropTargets:r({input:i,source:n.payload,target:t.target,current:[]})}}var Ut,B,Wt,Gt=e((()=>{vt(),Ut=O(),qe(),Ge(),kt(),jt(),Mt(),It(),B={isActive:!1},Wt={canStart:Lt,start:Bt}}));function Kt(e){var t=e.typeKey,n=e.mount,r=V.get(t);if(r)return r.usageCount++,r;var i={typeKey:t,unmount:n(),usageCount:1};return V.set(t,i),i}function qt(e){var t=Kt(e);return function(){t.usageCount--,!(t.usageCount>0)&&(t.unmount(),V.delete(e.typeKey))}}var V,Jt=e((()=>{V=new Map}));function Yt(){var e=[...arguments];return function(){e.forEach(function(e){return e()})}}var Xt=e((()=>{}));function Zt(e,t){var n=t.attribute,r=t.value;return e.setAttribute(n,r),function(){return e.removeAttribute(n)}}var Qt=e((()=>{}));function $t(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function H(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?$t(Object(n),!0).forEach(function(t){S(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):$t(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function en(e,t){var n=typeof Symbol<`u`&&e[Symbol.iterator]||e[`@@iterator`];if(!n){if(Array.isArray(e)||(n=tn(e))||t&&e&&typeof e.length==`number`){n&&(e=n);var r=0,i=function(){};return{s:i,n:function(){return r>=e.length?{done:!0}:{done:!1,value:e[r++]}},e:function(e){throw e},f:i}}throw TypeError(`Invalid attempt to iterate non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var a,o=!0,s=!1;return{s:function(){n=n.call(e)},n:function(){var e=n.next();return o=e.done,e},e:function(e){s=!0,a=e},f:function(){try{o||n.return==null||n.return()}finally{if(s)throw a}}}}function tn(e,t){if(e){if(typeof e==`string`)return nn(e,t);var n={}.toString.call(e).slice(8,-1);return n===`Object`&&e.constructor&&(n=e.constructor.name),n===`Map`||n===`Set`?Array.from(e):n===`Arguments`||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?nn(e,t):void 0}}function nn(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}function rn(e){return e.slice(0).reverse()}function an(e){var t=e.typeKey,n=e.defaultDropEffect,r=new WeakMap,i=`data-drop-target-for-${t}`,a=`[${i}]`;function o(e){return r.set(e.element,e),function(){return r.delete(e.element)}}function s(e){return k(Yt(Zt(e.element,{attribute:i,value:`true`}),o(e)))}function c(e){var t=e.source,i=e.target,o=e.input,s=e.result,l=s===void 0?[]:s;if(i==null)return l;if(!(i instanceof Element))return i instanceof Node?c({source:t,target:i.parentElement,input:o,result:l}):l;var u=i.closest(a);if(u==null)return l;var d=r.get(u);if(d==null)return l;var f={input:o,source:t,element:d.element};if(d.canDrop&&!d.canDrop(f))return c({source:t,target:d.element.parentElement,input:o,result:l});var p=d.getData?.call(d,f)??{},m=d.getDropEffect?.call(d,f)??n,h={data:p,element:d.element,dropEffect:m,isActiveDueToStickiness:!1};return c({source:t,target:d.element.parentElement,input:o,result:[].concat(_t(l),[h])})}function l(e){var t=e.eventName,n=e.payload,i=en(n.location.current.dropTargets),a;try{for(i.s();!(a=i.n()).done;){var o,s=a.value,c=r.get(s.element),l=H(H({},n),{},{self:s});c==null||(o=c[t])==null||o.call(c,l)}}catch(e){i.e(e)}finally{i.f()}}var u={onGenerateDragPreview:l,onDrag:l,onDragStart:l,onDrop:l,onDropTargetChange:function(e){var t=e.payload,n=new Set(t.location.current.dropTargets.map(function(e){return e.element})),i=new Set,a=en(t.location.previous.dropTargets),o;try{for(a.s();!(o=a.n()).done;){var s,c=o.value;i.add(c.element);var l=r.get(c.element),u=n.has(c.element),d=H(H({},t),{},{self:c});if(l==null||(s=l.onDropTargetChange)==null||s.call(l,d),!u){var f;l==null||(f=l.onDragLeave)==null||f.call(l,d)}}}catch(e){a.e(e)}finally{a.f()}var p=en(t.location.current.dropTargets),m;try{for(p.s();!(m=p.n()).done;){var h,g,_=m.value;if(!i.has(_.element)){var v=H(H({},t),{},{self:_}),y=r.get(_.element);y==null||(h=y.onDropTargetChange)==null||h.call(y,v),y==null||(g=y.onDragEnter)==null||g.call(y,v)}}}catch(e){p.e(e)}finally{p.f()}}};function d(e){u[e.eventName](e)}function f(e){var t=e.source,n=e.target,i=e.input,a=e.current,o=c({source:t,target:n,input:i});if(o.length>=a.length)return o;for(var s=rn(a),l=rn(o),u=[],d=0;d<s.length;d++){var f,p=s[d],m=l[d];if(m!=null){u.push(m);continue}var h=u[d-1],g=s[d-1];if(h?.element!==g?.element)break;var _=r.get(p.element);if(!_)break;var v={input:i,source:t,element:_.element};if(_.canDrop&&!_.canDrop(v)||!((f=_.getIsSticky)!=null&&f.call(_,v)))break;u.push(H(H({},p),{},{isActiveDueToStickiness:!0}))}return rn(u)}return{dropTargetForConsumers:s,getIsOver:f,dispatchEvent:d}}var on=e((()=>{C(),vt(),Xt(),A(),Qt()}));function sn(e,t){var n=typeof Symbol<`u`&&e[Symbol.iterator]||e[`@@iterator`];if(!n){if(Array.isArray(e)||(n=cn(e))||t&&e&&typeof e.length==`number`){n&&(e=n);var r=0,i=function(){};return{s:i,n:function(){return r>=e.length?{done:!0}:{done:!1,value:e[r++]}},e:function(e){throw e},f:i}}throw TypeError(`Invalid attempt to iterate non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var a,o=!0,s=!1;return{s:function(){n=n.call(e)},n:function(){var e=n.next();return o=e.done,e},e:function(e){s=!0,a=e},f:function(){try{o||n.return==null||n.return()}finally{if(s)throw a}}}}function cn(e,t){if(e){if(typeof e==`string`)return ln(e,t);var n={}.toString.call(e).slice(8,-1);return n===`Object`&&e.constructor&&(n=e.constructor.name),n===`Map`||n===`Set`?Array.from(e):n===`Arguments`||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?ln(e,t):void 0}}function ln(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}function un(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function dn(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?un(Object(n),!0).forEach(function(t){S(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):un(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function fn(){var e=new Set,t=null;function n(e){t&&(!e.canMonitor||e.canMonitor(t.canMonitorArgs))&&t.active.add(e)}function r(r){var i=dn({},r);e.add(i),n(i);function a(){e.delete(i),t&&t.active.delete(i)}return k(a)}function i(r){var i=r.eventName,a=r.payload;if(i===`onGenerateDragPreview`){t={canMonitorArgs:{initial:a.location.initial,source:a.source},active:new Set};var o=sn(e),s;try{for(o.s();!(s=o.n()).done;){var c=s.value;n(c)}}catch(e){o.e(e)}finally{o.f()}}if(t){for(var l=Array.from(t.active),u=0,d=l;u<d.length;u++){var f=d[u];if(t.active.has(f)){var p;(p=f[i])==null||p.call(f,a)}}i===`onDrop`&&(t.active.clear(),t=null)}}return{dispatchEvent:i,monitorForConsumers:r}}var pn=e((()=>{C(),A()}));function mn(e){var t=e.typeKey,n=e.mount,r=e.dispatchEventToSource,i=e.onPostDispatch,a=e.defaultDropEffect,o=fn(),s=an({typeKey:t,defaultDropEffect:a});function c(e){r?.(e),s.dispatchEvent(e),o.dispatchEvent(e),i?.(e)}function l(e){var t=e.event,n=e.dragType;Wt.start({event:t,dragType:n,getDropTargetsOver:s.getIsOver,dispatchEvent:c})}function u(){function e(){return n({canStart:Wt.canStart,start:l})}return qt({typeKey:t,mount:e})}return{registerUsage:u,dropTarget:s.dropTargetForConsumers,monitor:o.monitorForConsumers}}var hn=e((()=>{Gt(),Jt(),on(),pn()})),gn,_n,vn=e((()=>{A(),gn=k(function(){return navigator.userAgent.toLocaleLowerCase().includes(`android`)}),_n=`pdnd:android-fallback`})),yn,bn=e((()=>{yn=`text/plain`})),xn=e((()=>{})),Sn,Cn=e((()=>{Sn=`application/vnd.pdnd`}));function wn(e){return U.set(e.element,e),function(){U.delete(e.element)}}function Tn(e){return k(Yt(W.registerUsage(),wn(e),Zt(e.element,{attribute:`draggable`,value:`true`})))}var En,U,Dn,W,On,kn,An=e((()=>{ze(),En=O(),qe(),ut(),hn(),Xt(),A(),Qt(),vn(),Mt(),bn(),xn(),Cn(),U=new WeakMap,Dn=lt(),W=mn({typeKey:`element`,defaultDropEffect:`move`,mount:function(e){return Yt(Dn.bindEvents(),(0,En.bind)(document,{type:`dragstart`,listener:function(t){if(e.canStart(t)&&!t.defaultPrevented&&t.dataTransfer){var n=t.target;if(n instanceof HTMLElement){var r=U.get(n);if(r){var i=L(t),a={element:r.element,dragHandle:r.dragHandle??null,input:i};if(r.canDrag&&!r.canDrag(a)){t.preventDefault();return}if(r.dragHandle){var o=Ke({x:i.clientX,y:i.clientY});if(!r.dragHandle.contains(o)){t.preventDefault();return}}var s=r.getInitialDataForExternal?.call(r,a)??null;if(s)for(var c=0,l=Object.entries(s);c<l.length;c++){var u=Re(l[c],2),d=u[0],f=u[1];t.dataTransfer.setData(d,f??``)}gn()&&!t.dataTransfer.types.includes(`text/plain`)&&!t.dataTransfer.types.includes(`text/uri-list`)&&t.dataTransfer.setData(yn,_n),t.dataTransfer.setData(Sn,``);var p={type:`element`,payload:{element:r.element,dragHandle:r.dragHandle??null,data:r.getInitialData?.call(r,a)??{}},startedFrom:`internal`};e.start({event:t,dragType:p})}}}}}))},dispatchEventToSource:function(e){var t,n,r=e.eventName,i=e.payload;(t=U.get(i.source.element))==null||(n=t[r])==null||n.call(t,i)},onPostDispatch:Dn.getOnPostDispatch()}),On=W.dropTarget,kn=W.monitor})),jn=e((()=>{An()}));function Mn(e){var t=e.list,n=e.startIndex,r=e.finishIndex;if(n===-1||r===-1)return Array.from(t);var i=Array.from(t),a=Re(i.splice(n,1),1)[0];return i.splice(r,0,a),i}var Nn=e((()=>{ze()})),Pn=e((()=>{Nn()}));function G(e){let t=n(!1),r=e.enabled??n(!0);return m([e.element,()=>e.dragHandle?.value,r],([n,r,i],a,o)=>{!n||!i||o(Tn({element:n,dragHandle:r??void 0,canDrag:e.canDrag,getInitialData:e.getInitialData,onDragStart:()=>{t.value=!0},onDrop:()=>{t.value=!1}}))},{flush:`post`,immediate:!0}),{isDragging:t}}var Fn,In=e((()=>{jn(),a(),Fn=`csp-sortable-item`,G.__docgenInfo=Object.assign({displayName:G.name??G.__name},{exportName:`useDraggableElement`,displayName:`useDraggableElement`,type:2,props:[{name:`element`,global:!1,description:``,tags:[],required:!0,type:`Ref<HTMLElement, HTMLElement>`,declarations:[],schema:`Ref<HTMLElement, HTMLElement>`},{name:`dragHandle`,global:!1,description:``,tags:[],required:!1,type:`Ref<HTMLElement, HTMLElement>`,declarations:[],schema:`Ref<HTMLElement, HTMLElement>`},{name:`enabled`,global:!1,description:``,tags:[],required:!1,type:`Ref<boolean, boolean>`,declarations:[],schema:`Ref<boolean, boolean>`},{name:`canDrag`,global:!1,description:``,tags:[],required:!1,type:`() => boolean`,declarations:[],schema:{kind:`event`,type:`(): boolean`}},{name:`getInitialData`,global:!1,description:``,tags:[],required:!0,type:`() => Record<string, unknown>`,declarations:[],schema:{kind:`event`,type:`(): Record<string, unknown>`}}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/composables/dnd/useDraggableElement.ts`})}));function K(e){let t=n(!1),r=n(null),i=e.enabled??n(!0);return m([e.element,i],([n,i],a,o)=>{!n||!i||o(On({element:n,canDrop:({source:t})=>!(e.canDrop&&!e.canDrop(t.data)),getData:({input:t,element:n})=>me(e.getData({input:t,element:n}),{input:t,element:n,allowedEdges:[`top`,`bottom`]}),onDragEnter:({self:e})=>{t.value=!0,r.value=w(e.data)},onDrag:({self:e})=>{r.value=w(e.data)},onDragLeave:()=>{t.value=!1,r.value=null},onDrop:()=>{t.value=!1,r.value=null}}))},{flush:`post`,immediate:!0}),{isDraggedOver:t,closestEdge:r}}var Ln=e((()=>{_e(),jn(),a(),K.__docgenInfo=Object.assign({displayName:K.name??K.__name},{exportName:`useDropTargetElement`,displayName:`useDropTargetElement`,type:2,props:[{name:`element`,global:!1,description:``,tags:[],required:!0,type:`Ref<HTMLElement, HTMLElement>`,declarations:[],schema:`Ref<HTMLElement, HTMLElement>`},{name:`enabled`,global:!1,description:``,tags:[],required:!1,type:`Ref<boolean, boolean>`,declarations:[],schema:`Ref<boolean, boolean>`},{name:`canDrop`,global:!1,description:``,tags:[],required:!1,type:`(source: Record<string, unknown>) => boolean`,declarations:[],schema:{kind:`event`,type:`(source: Record<string, unknown>): boolean`}},{name:`getData`,global:!1,description:``,tags:[],required:!0,type:`(args: { input: Input; element: Element; }) => Record<string, unknown>`,declarations:[],schema:{kind:`event`,type:`(args: { input: Input; element: Element; }): Record<string, unknown>`}}],events:[],slots:[],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/composables/dnd/useDropTargetElement.ts`})})),Rn,zn,q,Bn=e((()=>{a(),In(),Ln(),Rn={key:0,class:`csp-sortable-list-item__indicator csp-sortable-list-item__indicator--top`},zn={key:1,class:`csp-sortable-list-item__indicator csp-sortable-list-item__indicator--bottom`},q=c({__name:`CspSortableListItem`,props:{item:{},itemId:{},index:{},listId:{},draggable:{type:Boolean,default:!0},disabled:{type:Boolean,default:!1}},setup(e){let t=e,r=n(null),a=n(null),o=u(()=>!t.disabled),c=u(()=>t.draggable&&o.value);function f(){return{type:Fn,listId:t.listId,itemId:t.itemId,index:t.index}}let{isDragging:p}=G({element:r,dragHandle:a,enabled:c,getInitialData:f}),{isDraggedOver:m,closestEdge:_}=K({element:r,enabled:o,canDrop:e=>e.type===`csp-sortable-item`&&e.listId===t.listId,getData:()=>f()});function v(e){a.value=e}return(n,a)=>(g(),s(`li`,{ref_key:`itemRef`,ref:r,class:i([`csp-sortable-list-item`,{"csp-sortable-list-item--dragging":l(p),"csp-sortable-list-item--drag-over":l(m)}])},[l(m)&&l(_)===`top`?(g(),s(`div`,Rn)):d(``,!0),h(n.$slots,`default`,{item:e.item,index:t.index,isDragging:l(p),isDraggedOver:l(m),closestEdge:l(_),setHandleRef:v,isDraggable:c.value},void 0,!0),l(m)&&l(_)===`bottom`?(g(),s(`div`,zn)):d(``,!0)],2))}})})),Vn=e((()=>{})),Hn,Un=e((()=>{Bn(),Bn(),Vn(),ee(),Hn=te(q,[[`__scopeId`,`data-v-15907b04`]]),q.__docgenInfo=Object.assign({displayName:q.name??q.__name},{exportName:`default`,displayName:`CspSortableListItem`,type:2,props:[{name:`item`,global:!1,description:``,tags:[],required:!0,type:`unknown`,declarations:[],schema:`unknown`},{name:`itemId`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`index`,global:!1,description:``,tags:[],required:!0,type:`number`,declarations:[],schema:`number`},{name:`listId`,global:!1,description:``,tags:[],required:!0,type:`string`,declarations:[],schema:`string`},{name:`draggable`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`true`},{name:`disabled`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[],slots:[{name:`default`,type:`{ item: unknown; index: number; isDragging: any; isDraggedOver: any; closestEdge: any; setHandleRef: (element: Element) => void; isDraggable: boolean; }`,description:``,declarations:[],schema:{kind:`object`,type:`{ item: unknown; index: number; isDragging: any; isDraggedOver: any; closestEdge: any; setHandleRef: (element: Element) => void; isDraggable: boolean; }`}}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspSortableList/CspSortableListItem.vue`})})),Wn,J,Gn=e((()=>{a(),_e(),ye(),De(),jn(),Pn(),In(),Un(),Wn={class:`csp-sortable-list`},J=c({__name:`CspSortableList`,props:{items:{},getItemKey:{},getItemLabel:{},isItemDraggable:{},disabled:{type:Boolean,default:!1}},emits:[`reorder`],setup(e,{emit:t}){let n=e,i=t,a=_();function c(e,t){return n.disabled?!1:n.isItemDraggable?.(e,t)??!0}function u(e){return n.getItemLabel?.(e)??n.getItemKey(e)}function d(e,t){if(n.disabled||t<0||t>=n.items.length||!c(n.items[e],e))return;i(`reorder`,Mn({list:n.items,startIndex:e,finishIndex:t}));let r=n.items[e];Te(`${u(r)} déplacé`)}function m(e){return()=>d(e,e-1)}function ee(e){return()=>d(e,e+1)}return v(()=>kn({canMonitor:({source:e})=>e.data.type===`csp-sortable-item`&&e.data.listId===a,onDrop:({source:e,location:t})=>{if(n.disabled)return;let r=t.current.dropTargets[0];if(!r)return;let a=e.data.index,o=r.data.index;if(typeof a!=`number`||typeof o!=`number`)return;let s=ve({startIndex:a,indexOfTarget:o,closestEdgeOfTarget:w(r.data),axis:`vertical`});if(s===a)return;i(`reorder`,Mn({list:n.items,startIndex:a,finishIndex:s}));let c=n.items[a];Te(`${u(c)} déplacé`)}})),(t,n)=>(g(),s(`ul`,Wn,[(g(!0),s(o,null,f(e.items,(n,i)=>(g(),r(Hn,{key:e.getItemKey(n),item:n,"item-id":e.getItemKey(n),index:i,"list-id":l(a),draggable:c(n,i),disabled:e.disabled},{default:y(r=>[h(t.$slots,`item`,p({ref_for:!0},r,{canMoveUp:c(n,i)&&i>0,canMoveDown:c(n,i)&&i<e.items.length-1,moveUp:m(i),moveDown:ee(i)}),void 0,!0)]),_:2},1032,[`item`,`item-id`,`index`,`list-id`,`draggable`,`disabled`]))),128))]))}})})),Kn=e((()=>{})),Y,qn=e((()=>{Gn(),Gn(),Kn(),ee(),Y=te(J,[[`__scopeId`,`data-v-d842298b`]]),J.__docgenInfo=Object.assign({displayName:J.name??J.__name},{exportName:`default`,displayName:`CspSortableList`,type:2,props:[{name:`items`,global:!1,description:``,tags:[],required:!0,type:`unknown[]`,declarations:[],schema:{kind:`array`,type:`unknown[]`}},{name:`getItemKey`,global:!1,description:``,tags:[],required:!0,type:`(item: unknown) => string`,declarations:[],schema:{kind:`event`,type:`(item: unknown): string`}},{name:`getItemLabel`,global:!1,description:``,tags:[],required:!1,type:`(item: unknown) => string`,declarations:[],schema:{kind:`event`,type:`(item: unknown): string`}},{name:`isItemDraggable`,global:!1,description:``,tags:[],required:!1,type:`(item: unknown, index: number) => boolean`,declarations:[],schema:{kind:`event`,type:`(item: unknown, index: number): boolean`}},{name:`disabled`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]},default:`false`},{name:`key`,global:!1,description:``,tags:[],required:!1,type:`PropertyKey`,declarations:[],schema:{kind:`enum`,type:`PropertyKey`,schema:[`string`,`number`,`symbol`]}},{name:`ref`,global:!1,description:``,tags:[],required:!1,type:`VNodeRef`,declarations:[],schema:{kind:`enum`,type:`VNodeRef`,schema:[`string`,`Ref<any, any>`,{kind:`event`,type:`(ref: Element | ComponentPublicInstance<{}, {}, {}, {}, {}, {}, {}, {}, false, ComponentOptionsBase<any, any, any, any, any, any, any, any, any, {}, {}, string, {}, {}, {}, string, ComponentProvideOptions>, ... 4 more ..., any>, refs: Record<...>): void`}]}},{name:`ref_for`,global:!1,description:``,tags:[],required:!1,type:`boolean`,declarations:[],schema:{kind:`enum`,type:`boolean`,schema:[`false`,`true`]}},{name:`ref_key`,global:!1,description:``,tags:[],required:!1,type:`string`,declarations:[],schema:`string`},{name:`class`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`},{name:`style`,global:!1,description:``,tags:[],required:!1,type:`unknown`,declarations:[],schema:`unknown`}],events:[{name:`reorder`,description:``,tags:[],type:`[items: unknown[]]`,signature:`(evt: "reorder", items: unknown[]): void`,declarations:[],schema:[{kind:`array`,type:`unknown[]`}]}],slots:[{name:`item`,type:`{ canMoveUp: boolean; canMoveDown: boolean; moveUp: () => void; moveDown: () => void; item: unknown; index: number; isDragging: any; isDraggedOver: any; closestEdge: any; setHandleRef: (element: Element) => void; isDraggable: boolean; }`,description:``,declarations:[],schema:{kind:`object`,type:`{ canMoveUp: boolean; canMoveDown: boolean; moveUp: () => void; moveDown: () => void; item: unknown; index: number; isDragging: any; isDraggedOver: any; closestEdge: any; setHandleRef: (element: Element) => void; isDraggable: boolean; }`}}],exposed:[],sourceFiles:`/home/runner/work/csplab/csplab/src/web/presentation/frontend/src/components/base/CspSortableList/CspSortableList.vue`})})),Jn,X,Yn,Xn,Z,Zn,Q,$,Qn;e((()=>{a(),re(),ae(),ne(),qn(),Jn={title:`Éléments/Génériques/CspSortableList`,component:Y,tags:[`autodocs`],parameters:{docs:{description:{component:"Liste réordonnables par drag and drop. Accessible via les fonctions `moveUp`/`moveDown` exposées dans le slot."}}},argTypes:{items:{control:!1,description:`Liste des éléments à afficher.`,table:{type:{summary:`T[]`}}},getItemKey:{control:!1,description:`Fonction retournant la clé unique de chaque élément.`,table:{type:{summary:`(item: T) => string`}}},getItemLabel:{control:!1,description:`Fonction retournant le libellé pour les annonces d'accessibilité.`,table:{type:{summary:`(item: T) => string`}}},isItemDraggable:{control:!1,description:`Fonction déterminant si un élément est déplaçable.`,table:{type:{summary:`(item: T, index: number) => boolean`},defaultValue:{summary:`() => true`}}},disabled:{control:{type:`boolean`},description:`Désactive le drag and drop sur toute la liste.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},onReorder:{action:`reorder`,description:`Émis quand la liste est réordonnée.`,table:{category:`Events`,type:{summary:`(items: T[]) => void`}}},item:{control:!1,description:"Slot pour personnaliser le rendu de chaque élément. Expose : `item`, `index`, `isDragging`, `isDraggable`, `setHandleRef`, `canMoveUp`, `canMoveDown`, `moveUp`, `moveDown`.",table:{category:`Slots`,type:{summary:`slot`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}}},X={display:`flex`,alignItems:`center`,gap:`var(--csp-space-3)`,padding:`var(--csp-space-3) var(--csp-space-4)`,borderRadius:`0.25rem`,boxShadow:`inset 0 0 0 1px var(--border-default-grey)`,background:`var(--background-default-grey)`},Yn={display:`flex`,cursor:`grab`,color:`var(--text-mention-grey)`},Xn={display:`flex`,color:`var(--text-mention-grey)`},Z={render:()=>({components:{CspSortableList:Y,CspIcon:b},setup(){let e=n([{id:`1`,label:`Élément 1`},{id:`2`,label:`Élément 2`},{id:`3`,label:`Élément 3`},{id:`4`,label:`Élément 4`}]);function t(t){e.value=t}return{items:e,itemStyle:X,handleStyle:Yn,getItemKey:e=>e.id,getItemLabel:e=>e.label,onReorder:t}},template:`
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        @reorder="onReorder"
      >
        <template #item="{ item, setHandleRef, isDragging }">
          <div :style="{ ...itemStyle, opacity: isDragging ? 0.5 : 1 }">
            <span :ref="setHandleRef" :style="handleStyle">
              <CspIcon name="ri:draggable" :size="16" />
            </span>
            <span style="flex: 1;">{{ item.label }}</span>
          </div>
        </template>
      </CspSortableList>
    `})},Zn={...X,background:`var(--background-disabled-grey)`,color:`var(--text-disabled-grey)`},Q={render:()=>({components:{CspSortableList:Y,CspIcon:b},setup(){let e=n([{id:`1`,label:`Élément épinglé`,pinned:!0},{id:`2`,label:`Élément 2`},{id:`3`,label:`Élément 3`},{id:`4`,label:`Élément 4`},{id:`5`,label:`Élément 5`}]);function t(t){t.findIndex(e=>e.pinned)===0&&(e.value=t)}return{items:e,itemStyle:X,pinnedItemStyle:Zn,iconStyle:Xn,getItemKey:e=>e.id,getItemLabel:e=>e.label,isItemDraggable:e=>!e.pinned,onReorder:t}},template:`
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        :is-item-draggable="isItemDraggable"
        @reorder="onReorder"
      >
        <template #item="{ item, setHandleRef, isDragging, isDraggable }">
          <div :style="{ ...(item.pinned ? pinnedItemStyle : itemStyle), opacity: isDragging ? 0.5 : 1 }">
            <span
              v-if="isDraggable"
              :ref="setHandleRef"
              :style="{ ...iconStyle, cursor: 'grab' }"
            >
              <CspIcon name="ri:draggable" :size="16" />
            </span>
            <span v-else :style="iconStyle">
              <CspIcon name="ri:pushpin-2-line" :size="16" />
            </span>
            <span style="flex: 1;">{{ item.label }}</span>
          </div>
        </template>
      </CspSortableList>
    `})},$={render:()=>({components:{CspSortableList:Y,CspIcon:b,CspButton:ie,CspDropdownMenu:oe},setup(){let e=n([{id:`1`,label:`Élément 1`},{id:`2`,label:`Élément 2`},{id:`3`,label:`Élément 3`},{id:`4`,label:`Élément 4`}]);function t(t){e.value=t}function r(t){e.value=e.value.filter(e=>e.id!==t)}function i(e,t,n,i,a){return[{items:[{label:`Monter`,icon:`ri:arrow-up-s-line`,disabled:!e,onSelect:n},{label:`Descendre`,icon:`ri:arrow-down-s-line`,disabled:!t,onSelect:i}]},{items:[{label:`Supprimer`,icon:`ri:delete-bin-line`,destructive:!0,onSelect:()=>r(a)}]}]}return{items:e,itemStyle:X,handleStyle:Yn,getItemKey:e=>e.id,getItemLabel:e=>e.label,onReorder:t,getMenuSections:i}},template:`
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        @reorder="onReorder"
      >
        <template #item="{ item, setHandleRef, isDragging, canMoveUp, canMoveDown, moveUp, moveDown }">
          <div :style="{ ...itemStyle, opacity: isDragging ? 0.5 : 1 }">
            <span :ref="setHandleRef" :style="handleStyle">
              <CspIcon name="ri:draggable" :size="16" />
            </span>
            <span style="flex: 1;">{{ item.label }}</span>
            <CspDropdownMenu
              :sections="getMenuSections(canMoveUp, canMoveDown, moveUp, moveDown, item.id)"
              side="bottom"
              align="end"
            >
              <template #trigger>
                <CspButton
                  icon="ri:more-2-fill"
                  variant="tertiary-no-outline"
                  size="sm"
                  aria-label="Actions"
                />
              </template>
            </CspDropdownMenu>
          </div>
        </template>
      </CspSortableList>
    `})},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSortableList,
      CspIcon
    },
    setup() {
      const items = ref<DemoItem[]>([{
        id: '1',
        label: 'Élément 1'
      }, {
        id: '2',
        label: 'Élément 2'
      }, {
        id: '3',
        label: 'Élément 3'
      }, {
        id: '4',
        label: 'Élément 4'
      }]);
      function onReorder(newItems: DemoItem[]) {
        items.value = newItems;
      }
      return {
        items,
        itemStyle,
        handleStyle,
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
        <template #item="{ item, setHandleRef, isDragging }">
          <div :style="{ ...itemStyle, opacity: isDragging ? 0.5 : 1 }">
            <span :ref="setHandleRef" :style="handleStyle">
              <CspIcon name="ri:draggable" :size="16" />
            </span>
            <span style="flex: 1;">{{ item.label }}</span>
          </div>
        </template>
      </CspSortableList>
    \`
  })
}`,...Z.parameters?.docs?.source}}},Q.parameters={...Q.parameters,docs:{...Q.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSortableList,
      CspIcon
    },
    setup() {
      const items = ref<PinnedDemoItem[]>([{
        id: '1',
        label: 'Élément épinglé',
        pinned: true
      }, {
        id: '2',
        label: 'Élément 2'
      }, {
        id: '3',
        label: 'Élément 3'
      }, {
        id: '4',
        label: 'Élément 4'
      }, {
        id: '5',
        label: 'Élément 5'
      }]);
      function onReorder(newItems: PinnedDemoItem[]) {
        const pinnedIndex = newItems.findIndex(item => item.pinned);
        if (pinnedIndex !== 0) return;
        items.value = newItems;
      }
      return {
        items,
        itemStyle,
        pinnedItemStyle,
        iconStyle,
        getItemKey: (item: PinnedDemoItem) => item.id,
        getItemLabel: (item: PinnedDemoItem) => item.label,
        isItemDraggable: (item: PinnedDemoItem) => !item.pinned,
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
        <template #item="{ item, setHandleRef, isDragging, isDraggable }">
          <div :style="{ ...(item.pinned ? pinnedItemStyle : itemStyle), opacity: isDragging ? 0.5 : 1 }">
            <span
              v-if="isDraggable"
              :ref="setHandleRef"
              :style="{ ...iconStyle, cursor: 'grab' }"
            >
              <CspIcon name="ri:draggable" :size="16" />
            </span>
            <span v-else :style="iconStyle">
              <CspIcon name="ri:pushpin-2-line" :size="16" />
            </span>
            <span style="flex: 1;">{{ item.label }}</span>
          </div>
        </template>
      </CspSortableList>
    \`
  })
}`,...Q.parameters?.docs?.source}}},$.parameters={...$.parameters,docs:{...$.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSortableList,
      CspIcon,
      CspButton,
      CspDropdownMenu
    },
    setup() {
      const items = ref<DemoItem[]>([{
        id: '1',
        label: 'Élément 1'
      }, {
        id: '2',
        label: 'Élément 2'
      }, {
        id: '3',
        label: 'Élément 3'
      }, {
        id: '4',
        label: 'Élément 4'
      }]);
      function onReorder(newItems: DemoItem[]) {
        items.value = newItems;
      }
      function removeItem(id: string) {
        items.value = items.value.filter(item => item.id !== id);
      }
      function getMenuSections(canMoveUp: boolean, canMoveDown: boolean, moveUp: () => void, moveDown: () => void, itemId: string) {
        return [{
          items: [{
            label: 'Monter',
            icon: 'ri:arrow-up-s-line',
            disabled: !canMoveUp,
            onSelect: moveUp
          }, {
            label: 'Descendre',
            icon: 'ri:arrow-down-s-line',
            disabled: !canMoveDown,
            onSelect: moveDown
          }]
        }, {
          items: [{
            label: 'Supprimer',
            icon: 'ri:delete-bin-line',
            destructive: true,
            onSelect: () => removeItem(itemId)
          }]
        }];
      }
      return {
        items,
        itemStyle,
        handleStyle,
        getItemKey: (item: DemoItem) => item.id,
        getItemLabel: (item: DemoItem) => item.label,
        onReorder,
        getMenuSections
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
              <CspIcon name="ri:draggable" :size="16" />
            </span>
            <span style="flex: 1;">{{ item.label }}</span>
            <CspDropdownMenu
              :sections="getMenuSections(canMoveUp, canMoveDown, moveUp, moveDown, item.id)"
              side="bottom"
              align="end"
            >
              <template #trigger>
                <CspButton
                  icon="ri:more-2-fill"
                  variant="tertiary-no-outline"
                  size="sm"
                  aria-label="Actions"
                />
              </template>
            </CspDropdownMenu>
          </div>
        </template>
      </CspSortableList>
    \`
  })
}`,...$.parameters?.docs?.source}}},Qn=[`Default`,`WithPinnedItems`,`WithActions`]}))();export{Z as Default,$ as WithActions,Q as WithPinnedItems,Qn as __namedExportsOrder,Jn as default};