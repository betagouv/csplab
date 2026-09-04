import{n as e,t}from"./rolldown-runtime-DkW27tQK.js";import{C as n,D as r,Dt as i,E as a,F as o,Q as s,R as c,S as l,U as u,V as d,W as f,Y as p,b as m,c as h,g,mt as _,nt as v,wt as y,x as ee,xt as b,y as x}from"./iframe-BUn2_ZZ6.js";import{n as S,t as te}from"./CspIcon-C23bgLJu.js";import{n as C,t as w}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as T,t as ne}from"./CspDropdownMenu-Baj8fO5u.js";import{n as re,t as ie}from"./CspButton-lulYhqad.js";function ae(e){var t=e.startIndex,n=e.closestEdgeOfTarget,r=e.indexOfTarget,i=e.axis;if(t===-1||r===-1||t===r)return t;if(n==null)return r;var a=i===`vertical`&&n===`bottom`||i===`horizontal`&&n===`right`;return t<r?a?r:r-1:a?r+1:r}var oe;function se(){return(se=e((()=>{oe=1e3})))()}function ce(){var e=document.createElement(`div`);return e.setAttribute(`role`,`status`),Object.assign(e.style,fe),document.body.append(e),e}function le(){return E===null&&(E=ce()),E}function ue(){O!==null&&clearTimeout(O),O=null}function de(e){le(),ue(),O=setTimeout(function(){O=null;var t=le();t.textContent=e},oe)}var E,D,fe,O;function pe(){return(pe=e((()=>{se(),E=null,D=`1px`,fe={width:D,height:D,padding:`0`,position:`absolute`,border:`0`,clip:`rect(${D}, ${D}, ${D}, ${D})`,overflow:`hidden`,whiteSpace:`nowrap`,marginTop:`-${D}`,pointerEvents:`none`},O=null})))()}function me(e){if(Array.isArray(e))return e}function he(e,t){var n=e==null?null:typeof Symbol<`u`&&e[Symbol.iterator]||e[`@@iterator`];if(n!=null){var r,i,a,o,s=[],c=!0,l=!1;try{if(a=(n=n.call(e)).next,t===0){if(Object(n)!==n)return;c=!1}else for(;!(c=(r=a.call(n)).done)&&(s.push(r.value),s.length!==t);c=!0);}catch(e){l=!0,i=e}finally{try{if(!c&&n.return!=null&&(o=n.return(),Object(o)!==o))return}finally{if(l)throw i}}return s}}function ge(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}function _e(e,t){if(e){if(typeof e==`string`)return ge(e,t);var n={}.toString.call(e).slice(8,-1);return n===`Object`&&e.constructor&&(n=e.constructor.name),n===`Map`||n===`Set`?Array.from(e):n===`Arguments`||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?ge(e,t):void 0}}function ve(){return(ve=e((()=>{})))()}function ye(){throw TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function be(e,t){return me(e)||he(e,t)||_e(e,t)||ye()}function k(){return(k=e((()=>{ve()})))()}var xe=t((e=>{Object.defineProperty(e,"__esModule",{value:!0}),e.bind=void 0;function t(e,t){var n=t.type,r=t.listener,i=t.options;return e.addEventListener(n,r,i),function(){e.removeEventListener(n,r,i)}}e.bind=t})),Se=t((e=>{var t=e&&e.__assign||function(){return t=Object.assign||function(e){for(var t,n=1,r=arguments.length;n<r;n++)for(var i in t=arguments[n],t)Object.prototype.hasOwnProperty.call(t,i)&&(e[i]=t[i]);return e},t.apply(this,arguments)};Object.defineProperty(e,"__esModule",{value:!0}),e.bindAll=void 0;var n=xe();function r(e){if(e!==void 0)return typeof e==`boolean`?{capture:e}:e}function i(e,n){return n==null?e:t(t({},e),{options:t(t({},r(n)),r(e.options))})}function a(e,t,r){var a=t.map(function(t){var a=i(t,r);return(0,n.bind)(e,a)});return function(){a.forEach(function(e){return e()})}}e.bindAll=a})),A=t((e=>{Object.defineProperty(e,"__esModule",{value:!0}),e.bindAll=e.bind=void 0;var t=xe();Object.defineProperty(e,"bind",{enumerable:!0,get:function(){return t.bind}});var n=Se();Object.defineProperty(e,"bindAll",{enumerable:!0,get:function(){return n.bindAll}})})),Ce;function we(){return(we=e((()=>{Ce=`data-pdnd-honey-pot`})))()}function Te(e){return e instanceof Element&&e.hasAttribute(`data-pdnd-honey-pot`)}function Ee(){return(Ee=e((()=>{we()})))()}function De(e){var t=be(document.elementsFromPoint(e.x,e.y),2),n=t[0],r=t[1];return n?Te(n)?r??null:n:null}function Oe(){return(Oe=e((()=>{k(),Ee()})))()}function j(e){"@babel/helpers - typeof";return j=typeof Symbol==`function`&&typeof Symbol.iterator==`symbol`?function(e){return typeof e}:function(e){return e&&typeof Symbol==`function`&&e.constructor===Symbol&&e!==Symbol.prototype?`symbol`:typeof e},j(e)}function ke(e,t){if(j(e)!=`object`||!e)return e;var n=e[Symbol.toPrimitive];if(n!==void 0){var r=n.call(e,t||`default`);if(j(r)!=`object`)return r;throw TypeError(`@@toPrimitive must return a primitive value.`)}return(t===`string`?String:Number)(e)}function Ae(){return(Ae=e((()=>{})))()}function je(e){var t=ke(e,`string`);return j(t)==`symbol`?t:t+``}function Me(){return(Me=e((()=>{Ae()})))()}function M(e,t,n){return(t=je(t))in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function N(){return(N=e((()=>{Me()})))()}var Ne;function Pe(){return(Pe=e((()=>{Ne=2147483647})))()}var Fe;function Ie(){return(Ie=e((()=>{Fe={inset:`unset`,border:`none`,padding:0,margin:0,overflow:`visible`,color:`inherit`,background:`transparent`,width:`auto`,height:`auto`}})))()}function P(e){var t=null;return function(){if(!t){var n=[...arguments];t={result:e.apply(this,n)}}return t.result}}var F;function Le(){return(Le=e((()=>{F=P(function(){return typeof HTMLElement<`u`&&typeof HTMLElement.prototype.showPopover==`function`})})))()}function Re(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function ze(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?Re(Object(n),!0).forEach(function(t){M(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):Re(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function Be(e){return{x:Math.floor(e.x),y:Math.floor(e.y)}}function Ve(e){return{x:e.x-Ye,y:e.y-Ye}}function He(e){return{x:Math.max(e.x,0),y:Math.max(e.y,0)}}function Ue(e){return{x:Math.min(e.x,window.innerWidth-L),y:Math.min(e.y,window.innerHeight-L)}}function We(e){var t=e.client,n=Ue(He(Ve(Be(t))));return DOMRect.fromRect({x:n.x,y:n.y,width:L,height:L})}function Ge(e){var t=e.clientRect;return{left:`${t.left}px`,top:`${t.top}px`,width:`${t.width}px`,height:`${t.height}px`}}function Ke(e){var t=e.client,n=e.clientRect;return t.x>=n.x&&t.x<=n.x+n.width&&t.y>=n.y&&t.y<=n.y+n.height}function qe(e){var t=e.initial,n=document.createElement(`div`);n.setAttribute(Ce,`true`),F()&&n.setAttribute(`popover`,`manual`);var r=We({client:t});Object.assign(n.style,ze(ze({position:`fixed`},F()?Fe:{zIndex:Ne}),{},{backgroundColor:`transparent`,padding:0,margin:0,boxSizing:`border-box`,pointerEvents:`auto`},Ge({clientRect:r}))),document.body.appendChild(n),F()&&n.showPopover();var i=(0,I.bind)(window,{type:`pointermove`,listener:function(e){r=We({client:{x:e.clientX,y:e.clientY}}),Object.assign(n.style,Ge({clientRect:r}))},options:{capture:!0}});return function(e){var t=e.current;if(i(),Ke({client:t,clientRect:r})){n.remove();return}function a(){o(),n.remove()}var o=(0,I.bindAll)(window,[{type:`pointerdown`,listener:a},{type:`pointermove`,listener:a},{type:`focusin`,listener:a},{type:`focusout`,listener:a},{type:`dragstart`,listener:a},{type:`dragenter`,listener:a},{type:`dragover`,listener:a}],{capture:!0})}}function Je(){var e=null;function t(){return e=null,(0,I.bind)(window,{type:`pointermove`,listener:function(t){e={x:t.clientX,y:t.clientY}},options:{capture:!0}})}function n(){var t=null;return function(n){var r=n.eventName,i=n.payload;if(r===`onDragStart`){var a=i.location.initial.input;t=qe({initial:e??{x:a.clientX,y:a.clientY}})}if(r===`onDrop`){var o,s=i.location.current.input;(o=t)==null||o({current:{x:s.clientX,y:s.clientY}}),t=null,e=null}}}return{bindEvents:t,getOnPostDispatch:n}}var I,L,Ye;function Xe(){return(Xe=e((()=>{N(),I=A(),Pe(),Ie(),Le(),we(),L=2,Ye=L/2})))()}function Ze(e){if(Array.isArray(e))return ge(e)}function Qe(){return(Qe=e((()=>{})))()}function $e(e){if(typeof Symbol<`u`&&e[Symbol.iterator]!=null||e[`@@iterator`]!=null)return Array.from(e)}function et(){throw TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function tt(e){return Ze(e)||$e(e)||_e(e)||et()}function nt(){return(nt=e((()=>{Qe(),ve()})))()}var rt;function it(){return(it=e((()=>{rt=P(function(){return navigator.userAgent.includes(`Firefox`)})})))()}var R;function at(){return(at=e((()=>{R=P(function(){var e=navigator.userAgent;return e.includes(`AppleWebKit`)&&!e.includes(`Chrome`)})})))()}function ot(e){var t=e.dragLeave;return R()?t.hasOwnProperty(z.isLeavingWindow):!1}var st,z;function ct(){return(ct=e((()=>{st=A(),at(),z={isLeavingWindow:Symbol(`leaving`),isEnteringWindow:Symbol(`entering`)},(function(){if(typeof window>`u`||!R())return;function e(){return{enterCount:0,isOverWindow:!1}}var t=e();function n(){t=e()}(0,st.bindAll)(window,[{type:`dragstart`,listener:function(){t.enterCount=0,t.isOverWindow=!0}},{type:`drop`,listener:n},{type:`dragend`,listener:n},{type:`dragenter`,listener:function(e){!t.isOverWindow&&t.enterCount===0&&(e[z.isEnteringWindow]=!0),t.isOverWindow=!0,t.enterCount++}},{type:`dragleave`,listener:function(e){t.enterCount--,t.isOverWindow&&t.enterCount===0&&(e[z.isLeavingWindow]=!0,t.isOverWindow=!1)}}],{capture:!0})})()})))()}function lt(e){return`nodeName`in e}function ut(e){return lt(e)&&e.ownerDocument!==document}function dt(e){var t=e.dragLeave,n=t.type,r=t.relatedTarget;return n===`dragleave`?R()?ot({dragLeave:t}):r==null?!0:rt()?ut(r):r instanceof HTMLIFrameElement:!1}function ft(){return(ft=e((()=>{it(),at(),ct()})))()}function pt(e){var t=e.onDragEnd;return[{type:`pointermove`,listener:function(){var e=0;return function(){if(e<20){e++;return}t()}}()},{type:`pointerdown`,listener:t}]}function B(e){return{altKey:e.altKey,button:e.button,buttons:e.buttons,ctrlKey:e.ctrlKey,metaKey:e.metaKey,shiftKey:e.shiftKey,clientX:e.clientX,clientY:e.clientY,pageX:e.pageX,pageY:e.pageY}}var mt;function ht(){return(ht=e((()=>{mt=function(e){var t=[],n=null,r=function(){t=[...arguments],!n&&(n=requestAnimationFrame(function(){n=null,e.apply(void 0,t)}))};return r.cancel=function(){n&&=(cancelAnimationFrame(n),null)},r}})))()}function gt(e){var t=e.source,n=e.initial,r=e.dispatchEvent,i={dropTargets:[]};function a(e){r(e),i={dropTargets:e.payload.location.current.dropTargets}}return{start:function(e){var r=e.nativeSetDragImage,o={current:n,previous:i,initial:n};a({eventName:`onGenerateDragPreview`,payload:{source:t,location:o,nativeSetDragImage:r}}),H.schedule(function(){a({eventName:`onDragStart`,payload:{source:t,location:o}})})},dragUpdate:function(e){var r=e.current;H.flush(),V.cancel(),a({eventName:`onDropTargetChange`,payload:{source:t,location:{initial:n,previous:i,current:r}}})},drag:function(e){var r=e.current;V(function(){H.flush(),a({eventName:`onDrag`,payload:{source:t,location:{initial:n,previous:i,current:r}}})})},drop:function(e){var r=e.current,o=e.updatedSourcePayload;H.flush(),V.cancel(),a({eventName:`onDrop`,payload:{source:o??t,location:{current:r,previous:i,initial:n}}})}}}var V,H;function _t(){return(_t=e((()=>{ht(),V=mt(function(e){return e()}),H=function(){var e=null;function t(t){e={frameId:requestAnimationFrame(function(){e=null,t()}),fn:t}}function n(){e&&=(cancelAnimationFrame(e.frameId),e.fn(),null)}return{schedule:t,flush:n}}()})))()}function vt(){return!U.isActive}function yt(e){return e.dataTransfer?e.dataTransfer.setDragImage.bind(e.dataTransfer):null}function bt(e){var t=e.current,n=e.next;if(t.length!==n.length)return!0;for(var r=0;r<t.length;r++)if(t[r].element!==n[r].element)return!0;return!1}function xt(e){var t=e.event,n=e.dragType,r=e.getDropTargetsOver,i=e.dispatchEvent;if(!vt())return;var a=Ct({event:t,dragType:n,getDropTargetsOver:r});U.isActive=!0;var o={current:a};St({event:t,current:a.dropTargets});var s=gt({source:n.payload,dispatchEvent:i,initial:a});function c(e){var t=bt({current:o.current.dropTargets,next:e.dropTargets});o.current=e,t&&s.dragUpdate({current:o.current})}function l(e){var t=B(e),i=r({target:Te(e.target)?De({x:t.clientX,y:t.clientY}):e.target,input:t,source:n.payload,current:o.current.dropTargets});i.length&&(e.preventDefault(),St({event:e,current:i})),c({dropTargets:i,input:t})}function u(){o.current.dropTargets.length&&c({dropTargets:[],input:o.current.input}),s.drop({current:o.current,updatedSourcePayload:null}),d()}function d(){U.isActive=!1,f()}var f=(0,wt.bindAll)(window,[{type:`dragover`,listener:function(e){l(e),s.drag({current:o.current})}},{type:`dragenter`,listener:l},{type:`dragleave`,listener:function(e){dt({dragLeave:e})&&(c({input:o.current.input,dropTargets:[]}),n.startedFrom===`external`&&u())}},{type:`drop`,listener:function(e){if(o.current={dropTargets:o.current.dropTargets,input:B(e)},!o.current.dropTargets.length){u();return}e.preventDefault(),St({event:e,current:o.current.dropTargets}),s.drop({current:o.current,updatedSourcePayload:n.type===`external`?n.getDropPayload(e):null}),d()}},{type:`dragend`,listener:function(e){o.current={dropTargets:o.current.dropTargets,input:B(e)},u()}}].concat(tt(pt({onDragEnd:u}))),{capture:!0});s.start({nativeSetDragImage:yt(t)})}function St(e){var t=e.event,n=e.current[0]?.dropEffect;n!=null&&t.dataTransfer&&(t.dataTransfer.dropEffect=n)}function Ct(e){var t=e.event,n=e.dragType,r=e.getDropTargetsOver,i=B(t);return n.startedFrom===`external`?{input:i,dropTargets:[]}:{input:i,dropTargets:r({input:i,source:n.payload,target:t.target,current:[]})}}var wt,U,Tt;function Et(){return(Et=e((()=>{nt(),wt=A(),Oe(),Ee(),ft(),_t(),U={isActive:!1},Tt={canStart:vt,start:xt}})))()}function Dt(e){var t=e.typeKey,n=e.mount,r=W.get(t);if(r)return r.usageCount++,r;var i={typeKey:t,unmount:n(),usageCount:1};return W.set(t,i),i}function Ot(e){var t=Dt(e);return function(){t.usageCount--,!(t.usageCount>0)&&(t.unmount(),W.delete(e.typeKey))}}var W;function kt(){return(kt=e((()=>{W=new Map})))()}function At(){var e=[...arguments];return function(){e.forEach(function(e){return e()})}}function jt(e,t){var n=t.attribute,r=t.value;return e.setAttribute(n,r),function(){return e.removeAttribute(n)}}function Mt(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function G(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?Mt(Object(n),!0).forEach(function(t){M(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):Mt(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function Nt(e,t){var n=typeof Symbol<`u`&&e[Symbol.iterator]||e[`@@iterator`];if(!n){if(Array.isArray(e)||(n=Pt(e))||t&&e&&typeof e.length==`number`){n&&(e=n);var r=0,i=function(){};return{s:i,n:function(){return r>=e.length?{done:!0}:{done:!1,value:e[r++]}},e:function(e){throw e},f:i}}throw TypeError(`Invalid attempt to iterate non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var a,o=!0,s=!1;return{s:function(){n=n.call(e)},n:function(){var e=n.next();return o=e.done,e},e:function(e){s=!0,a=e},f:function(){try{o||n.return==null||n.return()}finally{if(s)throw a}}}}function Pt(e,t){if(e){if(typeof e==`string`)return Ft(e,t);var n={}.toString.call(e).slice(8,-1);return n===`Object`&&e.constructor&&(n=e.constructor.name),n===`Map`||n===`Set`?Array.from(e):n===`Arguments`||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?Ft(e,t):void 0}}function Ft(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}function It(e){return e.slice(0).reverse()}function Lt(e){var t=e.typeKey,n=e.defaultDropEffect,r=new WeakMap,i=`data-drop-target-for-${t}`,a=`[${i}]`;function o(e){return r.set(e.element,e),function(){return r.delete(e.element)}}function s(e){return P(At(jt(e.element,{attribute:i,value:`true`}),o(e)))}function c(e){var t=e.source,i=e.target,o=e.input,s=e.result,l=s===void 0?[]:s;if(i==null)return l;if(!(i instanceof Element))return i instanceof Node?c({source:t,target:i.parentElement,input:o,result:l}):l;var u=i.closest(a);if(u==null)return l;var d=r.get(u);if(d==null)return l;var f={input:o,source:t,element:d.element};if(d.canDrop&&!d.canDrop(f))return c({source:t,target:d.element.parentElement,input:o,result:l});var p=d.getData?.call(d,f)??{},m=d.getDropEffect?.call(d,f)??n,h={data:p,element:d.element,dropEffect:m,isActiveDueToStickiness:!1};return c({source:t,target:d.element.parentElement,input:o,result:[].concat(tt(l),[h])})}function l(e){var t=e.eventName,n=e.payload,i=Nt(n.location.current.dropTargets),a;try{for(i.s();!(a=i.n()).done;){var o,s=a.value,c=r.get(s.element),l=G(G({},n),{},{self:s});c==null||(o=c[t])==null||o.call(c,l)}}catch(e){i.e(e)}finally{i.f()}}var u={onGenerateDragPreview:l,onDrag:l,onDragStart:l,onDrop:l,onDropTargetChange:function(e){var t=e.payload,n=new Set(t.location.current.dropTargets.map(function(e){return e.element})),i=new Set,a=Nt(t.location.previous.dropTargets),o;try{for(a.s();!(o=a.n()).done;){var s,c=o.value;i.add(c.element);var l=r.get(c.element),u=n.has(c.element),d=G(G({},t),{},{self:c});if(l==null||(s=l.onDropTargetChange)==null||s.call(l,d),!u){var f;l==null||(f=l.onDragLeave)==null||f.call(l,d)}}}catch(e){a.e(e)}finally{a.f()}var p=Nt(t.location.current.dropTargets),m;try{for(p.s();!(m=p.n()).done;){var h,g,_=m.value;if(!i.has(_.element)){var v=G(G({},t),{},{self:_}),y=r.get(_.element);y==null||(h=y.onDropTargetChange)==null||h.call(y,v),y==null||(g=y.onDragEnter)==null||g.call(y,v)}}}catch(e){p.e(e)}finally{p.f()}}};function d(e){u[e.eventName](e)}function f(e){var t=e.source,n=e.target,i=e.input,a=e.current,o=c({source:t,target:n,input:i});if(o.length>=a.length)return o;for(var s=It(a),l=It(o),u=[],d=0;d<s.length;d++){var f,p=s[d],m=l[d];if(m!=null){u.push(m);continue}var h=u[d-1],g=s[d-1];if(h?.element!==g?.element)break;var _=r.get(p.element);if(!_)break;var v={input:i,source:t,element:_.element};if(_.canDrop&&!_.canDrop(v)||!((f=_.getIsSticky)!=null&&f.call(_,v)))break;u.push(G(G({},p),{},{isActiveDueToStickiness:!0}))}return It(u)}return{dropTargetForConsumers:s,getIsOver:f,dispatchEvent:d}}function Rt(){return(Rt=e((()=>{N(),nt()})))()}function zt(e,t){var n=typeof Symbol<`u`&&e[Symbol.iterator]||e[`@@iterator`];if(!n){if(Array.isArray(e)||(n=Bt(e))||t&&e&&typeof e.length==`number`){n&&(e=n);var r=0,i=function(){};return{s:i,n:function(){return r>=e.length?{done:!0}:{done:!1,value:e[r++]}},e:function(e){throw e},f:i}}throw TypeError(`Invalid attempt to iterate non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var a,o=!0,s=!1;return{s:function(){n=n.call(e)},n:function(){var e=n.next();return o=e.done,e},e:function(e){s=!0,a=e},f:function(){try{o||n.return==null||n.return()}finally{if(s)throw a}}}}function Bt(e,t){if(e){if(typeof e==`string`)return Vt(e,t);var n={}.toString.call(e).slice(8,-1);return n===`Object`&&e.constructor&&(n=e.constructor.name),n===`Map`||n===`Set`?Array.from(e):n===`Arguments`||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?Vt(e,t):void 0}}function Vt(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}function Ht(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function Ut(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?Ht(Object(n),!0).forEach(function(t){M(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):Ht(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function Wt(){var e=new Set,t=null;function n(e){t&&(!e.canMonitor||e.canMonitor(t.canMonitorArgs))&&t.active.add(e)}function r(r){var i=Ut({},r);e.add(i),n(i);function a(){e.delete(i),t&&t.active.delete(i)}return P(a)}function i(r){var i=r.eventName,a=r.payload;if(i===`onGenerateDragPreview`){t={canMonitorArgs:{initial:a.location.initial,source:a.source},active:new Set};var o=zt(e),s;try{for(o.s();!(s=o.n()).done;){var c=s.value;n(c)}}catch(e){o.e(e)}finally{o.f()}}if(t){for(var l=Array.from(t.active),u=0,d=l;u<d.length;u++){var f=d[u];if(t.active.has(f)){var p;(p=f[i])==null||p.call(f,a)}}i===`onDrop`&&(t.active.clear(),t=null)}}return{dispatchEvent:i,monitorForConsumers:r}}function Gt(){return(Gt=e((()=>{N()})))()}function Kt(e){var t=e.typeKey,n=e.mount,r=e.dispatchEventToSource,i=e.onPostDispatch,a=e.defaultDropEffect,o=Wt(),s=Lt({typeKey:t,defaultDropEffect:a});function c(e){r?.(e),s.dispatchEvent(e),o.dispatchEvent(e),i?.(e)}function l(e){var t=e.event,n=e.dragType;Tt.start({event:t,dragType:n,getDropTargetsOver:s.getIsOver,dispatchEvent:c})}function u(){function e(){return n({canStart:Tt.canStart,start:l})}return Ot({typeKey:t,mount:e})}return{registerUsage:u,dropTarget:s.dropTargetForConsumers,monitor:o.monitorForConsumers}}function qt(){return(qt=e((()=>{Et(),kt(),Rt(),Gt()})))()}var Jt,Yt;function Xt(){return(Xt=e((()=>{Jt=P(function(){return navigator.userAgent.toLocaleLowerCase().includes(`android`)}),Yt=`pdnd:android-fallback`})))()}var Zt;function Qt(){return(Qt=e((()=>{Zt=`text/plain`})))()}function $t(){return($t=e((()=>{})))()}var en;function tn(){return(tn=e((()=>{en=`application/vnd.pdnd`})))()}function nn(e){return K.set(e.element,e),function(){K.delete(e.element)}}function rn(e){return P(At(q.registerUsage(),nn(e),jt(e.element,{attribute:`draggable`,value:`true`})))}var an,K,on,q,sn,cn;function ln(){return(ln=e((()=>{k(),an=A(),Oe(),Xe(),qt(),Xt(),Qt(),$t(),tn(),K=new WeakMap,on=Je(),q=Kt({typeKey:`element`,defaultDropEffect:`move`,mount:function(e){return At(on.bindEvents(),(0,an.bind)(document,{type:`dragstart`,listener:function(t){if(e.canStart(t)&&!t.defaultPrevented&&t.dataTransfer){var n=t.target;if(n instanceof HTMLElement){var r=K.get(n);if(r){var i=B(t),a={element:r.element,dragHandle:r.dragHandle??null,input:i};if(r.canDrag&&!r.canDrag(a)){t.preventDefault();return}if(r.dragHandle){var o=De({x:i.clientX,y:i.clientY});if(!r.dragHandle.contains(o)){t.preventDefault();return}}var s=r.getInitialDataForExternal?.call(r,a)??null;if(s)for(var c=0,l=Object.entries(s);c<l.length;c++){var u=be(l[c],2),d=u[0],f=u[1];t.dataTransfer.setData(d,f??``)}Jt()&&!t.dataTransfer.types.includes(`text/plain`)&&!t.dataTransfer.types.includes(`text/uri-list`)&&t.dataTransfer.setData(Zt,Yt),t.dataTransfer.setData(en,``);var p={type:`element`,payload:{element:r.element,dragHandle:r.dragHandle??null,data:r.getInitialData?.call(r,a)??{}},startedFrom:`internal`};e.start({event:t,dragType:p})}}}}}))},dispatchEventToSource:function(e){var t,n,r=e.eventName,i=e.payload;(t=K.get(i.source.element))==null||(n=t[r])==null||n.call(t,i)},onPostDispatch:on.getOnPostDispatch()}),sn=q.dropTarget,cn=q.monitor})))()}function J(){return(J=e((()=>{ln()})))()}function un(e){var t=e.list,n=e.startIndex,r=e.finishIndex;if(n===-1||r===-1)return Array.from(t);var i=Array.from(t),a=be(i.splice(n,1),1)[0];return i.splice(r,0,a),i}function dn(){return(dn=e((()=>{k()})))()}function fn(e){let t=_(!1),n=e.enabled??_(!0);return s([e.element,()=>e.dragHandle?.value,n],([n,r,i],a,o)=>{!n||!i||o(rn({element:n,dragHandle:r??void 0,canDrag:e.canDrag,getInitialData:e.getInitialData,onDragStart:()=>{t.value=!0},onDrop:()=>{t.value=!1}}))},{flush:`post`,immediate:!0}),{isDragging:t}}var pn;function mn(){return(mn=e((()=>{J(),h(),pn=`csp-sortable-item`})))()}function hn(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function gn(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?hn(Object(n),!0).forEach(function(t){M(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):hn(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function _n(e,t){var n=t.element,r=t.input,i=t.allowedEdges,a={x:r.clientX,y:r.clientY},o=n.getBoundingClientRect(),s=i.map(function(e){return{edge:e,value:vn[e](o,a)}}).sort(function(e,t){return e.value-t.value})[0]?.edge??null;return gn(gn({},e),{},M({},Sn,s))}var vn;function yn(){return(yn=e((()=>{N(),Y(),vn={top:function(e,t){return Math.abs(t.y-e.top)},right:function(e,t){return Math.abs(e.right-t.x)},bottom:function(e,t){return Math.abs(e.bottom-t.y)},left:function(e,t){return Math.abs(t.x-e.left)}}})))()}function bn(e){return e[Sn]??null}function xn(){return(xn=e((()=>{Y()})))()}var Sn;function Y(){return(Y=e((()=>{yn(),xn(),Sn=Symbol(`closestEdge`)})))()}function Cn(e){let t=_(!1),n=_(null),r=_(null),i=e.enabled??_(!0);return s([e.element,i],([i,a],o,s)=>{!i||!a||s(sn({element:i,canDrop:({source:t})=>!(e.canDrop&&!e.canDrop(t.data)),getData:({input:t,element:n})=>_n(e.getData({input:t,element:n}),{input:t,element:n,allowedEdges:[`top`,`bottom`]}),onDragEnter:({self:e,source:i})=>{t.value=!0,n.value=bn(e.data),r.value=typeof i.data.index==`number`?i.data.index:null},onDrag:({self:e})=>{n.value=bn(e.data)},onDragLeave:()=>{t.value=!1,n.value=null,r.value=null},onDrop:()=>{t.value=!1,n.value=null,r.value=null}}))},{flush:`post`,immediate:!0}),{isDraggedOver:t,closestEdge:n,sourceIndex:r}}function wn(){return(wn=e((()=>{Y(),J(),h()})))()}var Tn,En,Dn,On,kn,An;function jn(){return(jn=e((()=>{h(),S(),mn(),wn(),Tn={key:0,class:`csp-sortable-list-item__indicator csp-sortable-list-item__indicator--top`},En={key:2,class:`csp-sortable-list-item__handle-spacer`,"aria-hidden":`true`},Dn={class:`csp-sortable-list-item__content`},On={key:0,class:`csp-sortable-list-item__position`},kn={key:3,class:`csp-sortable-list-item__indicator csp-sortable-list-item__indicator--bottom`},An=r({__name:`CspSortableListItem`,props:{item:{},itemId:{},index:{},listId:{},draggable:{type:Boolean,default:!0},disabled:{type:Boolean,default:!1},variant:{default:`default`},showPosition:{type:Boolean,default:!1}},setup(e){let t=e,r=_(null),o=_(null),s=x(()=>!t.disabled),c=x(()=>t.draggable&&s.value);function u(){return{type:pn,listId:t.listId,itemId:t.itemId,index:t.index}}let{isDragging:p}=fn({element:r,dragHandle:o,enabled:c,getInitialData:u}),{isDraggedOver:h,sourceIndex:g}=Cn({element:r,enabled:c,canDrop:e=>e.type===`csp-sortable-item`&&e.listId===t.listId&&e.itemId!==t.itemId,getData:()=>u()}),v=x(()=>g.value!==null&&g.value<t.index),ee=x(()=>g.value!==null&&g.value>t.index),S=x(()=>h.value&&ee.value),C=x(()=>h.value&&v.value),w=x(()=>S.value?`top`:C.value?`bottom`:null);function T(e){o.value=e}return(o,s)=>(d(),n(`li`,{ref_key:`itemRef`,ref:r,class:y([`csp-sortable-list-item`,[`csp-sortable-list-item--${e.variant}`,{"csp-sortable-list-item--dragging":b(p),"csp-sortable-list-item--drag-over":b(h)}]])},[S.value?(d(),n(`div`,Tn)):l(``,!0),c.value?(d(),n(`span`,{key:1,ref:e=>T(e),class:`csp-sortable-list-item__handle`},[a(te,{name:`ri:draggable`,size:16})],512)):(d(),n(`span`,En)),m(`div`,Dn,[e.showPosition?(d(),n(`span`,On,i(e.index+1),1)):l(``,!0),f(o.$slots,`default`,{item:e.item,index:t.index,isDragging:b(p),isDraggedOver:b(h),closestEdge:w.value,setHandleRef:T,isDraggable:c.value},void 0,!0)]),C.value?(d(),n(`div`,kn)):l(``,!0)],2))}})})))()}var Mn;function Nn(){return(Nn=e((()=>{jn(),C(),Mn=w(An,[[`__scopeId`,`data-v-c0741aae`]])})))()}var Pn,Fn,In,Ln,Rn;function zn(){return(zn=e((()=>{h(),pe(),J(),dn(),mn(),Nn(),Pn={class:`csp-sortable-list`},Fn={key:0,class:`csp-sortable-list__header`},In={class:`csp-sortable-list__header-content`},Ln={class:`csp-sortable-list__items`},Rn=r({__name:`CspSortableList`,props:{items:{},getItemKey:{},getItemLabel:{},isItemDraggable:{},getItemVariant:{},disabled:{type:Boolean,default:!1},showPosition:{type:Boolean,default:!1}},emits:[`reorder`],setup(e,{emit:t}){let r=e,i=t,a=p();function s(e,t){return r.disabled?!1:r.isItemDraggable?.(e,t)??!0}function h(e,t){return r.getItemVariant?.(e,t)??`default`}function _(e){return r.getItemLabel?.(e)??r.getItemKey(e)}function y(e){for(let t=0;t<r.items.length;t++){let n=r.items[t];if(!s(n,t)&&r.getItemKey(e[t])!==r.getItemKey(n))return!1}return!0}function x(e,t){if(r.disabled||e===t||t<0||t>=r.items.length||!s(r.items[e],e))return;let n=un({list:r.items,startIndex:e,finishIndex:t});y(n)&&(i(`reorder`,n),de(`${_(r.items[e])} déplacé`))}function S(e){return e<=0||!s(r.items[e],e)?!1:s(r.items[e-1],e-1)}function te(e){return e>=r.items.length-1||!s(r.items[e],e)?!1:s(r.items[e+1],e+1)}function C(e){return()=>x(e,e-1)}function w(e){return()=>x(e,e+1)}return c(()=>cn({canMonitor:({source:e})=>e.data.type===`csp-sortable-item`&&e.data.listId===a,onDrop:({source:e,location:t})=>{if(r.disabled)return;let n=t.current.dropTargets[0];if(!n)return;let i=e.data.index,a=n.data.index;typeof i==`number`&&typeof a==`number`&&x(i,ae({startIndex:i,indexOfTarget:a,closestEdgeOfTarget:a>i?`bottom`:`top`,axis:`vertical`}))}})),(t,r)=>(d(),n(`div`,Pn,[t.$slots.header?(d(),n(`div`,Fn,[r[0]||=m(`span`,{class:`csp-sortable-list__header-handle-spacer`,"aria-hidden":`true`},null,-1),m(`div`,In,[f(t.$slots,`header`,{},void 0,!0)])])):l(``,!0),m(`ul`,Ln,[(d(!0),n(g,null,u(e.items,(n,r)=>(d(),ee(Mn,{key:e.getItemKey(n),item:n,"item-id":e.getItemKey(n),index:r,"list-id":b(a),draggable:s(n,r),variant:h(n,r),disabled:e.disabled,"show-position":e.showPosition},{default:v(e=>[f(t.$slots,`item`,o({ref_for:!0},e,{canMoveUp:S(r),canMoveDown:te(r),moveUp:C(r),moveDown:w(r)}),void 0,!0)]),_:2},1032,[`item`,`item-id`,`index`,`list-id`,`draggable`,`variant`,`disabled`,`show-position`]))),128))])]))}})})))()}var X;function Bn(){return(Bn=e((()=>{zn(),C(),X=w(Rn,[[`__scopeId`,`data-v-82abd474`]])})))()}var Vn,Z,Q,$,Hn;function Un(){return(Un=e((()=>{h(),re(),T(),Bn(),Vn={title:`Éléments/Génériques/CspSortableList`,component:X,tags:[`autodocs`],parameters:{docs:{description:{component:"Liste réordonnable par drag and drop. Accessible via les fonctions `moveUp`/`moveDown` exposées dans le slot."}}},argTypes:{items:{control:!1,description:`Liste des éléments à afficher.`,table:{type:{summary:`T[]`}}},getItemKey:{control:!1,description:`Fonction retournant la clé unique de chaque élément.`,table:{type:{summary:`(item: T) => string`}}},getItemLabel:{control:!1,description:`Fonction retournant le libellé pour les annonces d'accessibilité.`,table:{type:{summary:`(item: T) => string`}}},isItemDraggable:{control:!1,description:`Fonction déterminant si un élément est déplaçable.`,table:{type:{summary:`(item: T, index: number) => boolean`},defaultValue:{summary:`() => true`}}},getItemVariant:{control:!1,description:`Fonction retournant la variante visuelle de chaque élément.`,table:{type:{summary:`(item: T, index: number) => 'default' | 'alt'`},defaultValue:{summary:`() => 'default'`}}},disabled:{control:{type:`boolean`},description:`Désactive le drag and drop sur toute la liste.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},onReorder:{action:`reorder`,description:`Émis quand la liste est réordonnée.`,table:{category:`Events`,type:{summary:`(items: T[]) => void`}}},item:{control:!1,description:"Slot pour personnaliser le contenu de chaque élément. Expose : `item`, `index`, `isDragging`, `isDraggable`, `canMoveUp`, `canMoveDown`, `moveUp`, `moveDown`.",table:{category:`Slots`,type:{summary:`slot`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}}},Z={render:()=>({components:{CspSortableList:X},setup(){let e=_([{id:`1`,label:`Élément 1`},{id:`2`,label:`Élément 2`},{id:`3`,label:`Élément 3`},{id:`4`,label:`Élément 4`}]);function t(t){e.value=t}return{items:e,getItemKey:e=>e.id,getItemLabel:e=>e.label,onReorder:t}},template:`
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        @reorder="onReorder"
      >
        <template #item="{ item }">
          <span style="flex: 1;">{{ item.label }}</span>
        </template>
      </CspSortableList>
    `})},Q={render:()=>({components:{CspSortableList:X},setup(){let e=_([{id:`1`,label:`Élément épinglé`,pinned:!0},{id:`2`,label:`Élément 2`},{id:`3`,label:`Élément 3`},{id:`4`,label:`Élément 4`},{id:`5`,label:`Élément 5`}]);function t(t){t.findIndex(e=>e.pinned)===0&&(e.value=t)}return{items:e,getItemKey:e=>e.id,getItemLabel:e=>e.label,isItemDraggable:e=>!e.pinned,getItemVariant:e=>e.pinned?`alt`:`default`,onReorder:t}},template:`
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        :is-item-draggable="isItemDraggable"
        :get-item-variant="getItemVariant"
        @reorder="onReorder"
      >
        <template #item="{ item }">
          <span style="flex: 1;">{{ item.label }}</span>
        </template>
      </CspSortableList>
    `})},$={render:()=>({components:{CspSortableList:X,CspButton:ie,CspDropdownMenu:ne},setup(){let e=_([{id:`1`,label:`Élément 1`},{id:`2`,label:`Élément 2`},{id:`3`,label:`Élément 3`},{id:`4`,label:`Élément 4`}]);function t(t){e.value=t}function n(t){e.value=e.value.filter(e=>e.id!==t)}function r(e,t,r,i,a){return[{items:[{label:`Monter`,icon:`ri:arrow-up-s-line`,disabled:!e,onSelect:r},{label:`Descendre`,icon:`ri:arrow-down-s-line`,disabled:!t,onSelect:i}]},{items:[{label:`Supprimer`,icon:`ri:delete-bin-line`,destructive:!0,onSelect:()=>n(a)}]}]}return{items:e,getItemKey:e=>e.id,getItemLabel:e=>e.label,onReorder:t,getMenuSections:r}},template:`
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        @reorder="onReorder"
      >
        <template #item="{ item, canMoveUp, canMoveDown, moveUp, moveDown }">
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
        </template>
      </CspSortableList>
    `})},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSortableList
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
        <template #item="{ item }">
          <span style="flex: 1;">{{ item.label }}</span>
        </template>
      </CspSortableList>
    \`
  })
}`,...Z.parameters?.docs?.source}}},Q.parameters={...Q.parameters,docs:{...Q.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSortableList
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
        getItemKey: (item: PinnedDemoItem) => item.id,
        getItemLabel: (item: PinnedDemoItem) => item.label,
        isItemDraggable: (item: PinnedDemoItem) => !item.pinned,
        getItemVariant: (item: PinnedDemoItem) => item.pinned ? 'alt' : 'default',
        onReorder
      };
    },
    template: \`
      <CspSortableList
        :items="items"
        :get-item-key="getItemKey"
        :get-item-label="getItemLabel"
        :is-item-draggable="isItemDraggable"
        :get-item-variant="getItemVariant"
        @reorder="onReorder"
      >
        <template #item="{ item }">
          <span style="flex: 1;">{{ item.label }}</span>
        </template>
      </CspSortableList>
    \`
  })
}`,...Q.parameters?.docs?.source}}},$.parameters={...$.parameters,docs:{...$.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspSortableList,
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
        <template #item="{ item, canMoveUp, canMoveDown, moveUp, moveDown }">
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
        </template>
      </CspSortableList>
    \`
  })
}`,...$.parameters?.docs?.source}}},Hn=[`Default`,`WithPinnedItems`,`WithActions`]})))()}Un();export{Z as Default,$ as WithActions,Q as WithPinnedItems,Hn as __namedExportsOrder,Vn as default};