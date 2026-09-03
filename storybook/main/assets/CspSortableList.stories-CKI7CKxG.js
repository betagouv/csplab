import{n as e,t}from"./rolldown-runtime-DkW27tQK.js";import{$ as n,C as r,D as i,G as a,H as o,I as s,O as c,Ot as l,S as u,St as d,Tt as f,W as p,X as m,_ as h,b as g,c as _,ht as v,rt as y,w as b,x,z as ee}from"./iframe-BrU2M-Uz.js";import{n as S,t as te}from"./CspIcon-CvpvdqQX.js";import{n as C,t as w}from"./_plugin-vue_export-helper-BqBa3wPr.js";import{n as ne,t as re}from"./CspDropdownMenu-Bwscn1zv.js";import{n as ie,t as ae}from"./CspButton-CxiQ4DQ7.js";function oe(e){var t=e.startIndex,n=e.closestEdgeOfTarget,r=e.indexOfTarget,i=e.axis;if(t===-1||r===-1||t===r)return t;if(n==null)return r;var a=i===`vertical`&&n===`bottom`||i===`horizontal`&&n===`right`;return t<r?a?r:r-1:a?r+1:r}var se;function ce(){return(ce=e((()=>{se=1e3})))()}function le(){var e=document.createElement(`div`);return e.setAttribute(`role`,`status`),Object.assign(e.style,pe),document.body.append(e),e}function ue(){return T===null&&(T=le()),T}function de(){D!==null&&clearTimeout(D),D=null}function fe(e){ue(),de(),D=setTimeout(function(){D=null;var t=ue();t.textContent=e},se)}var T,E,pe,D;function me(){return(me=e((()=>{ce(),T=null,E=`1px`,pe={width:E,height:E,padding:`0`,position:`absolute`,border:`0`,clip:`rect(${E}, ${E}, ${E}, ${E})`,overflow:`hidden`,whiteSpace:`nowrap`,marginTop:`-${E}`,pointerEvents:`none`},D=null})))()}function he(e){if(Array.isArray(e))return e}function ge(e,t){var n=e==null?null:typeof Symbol<`u`&&e[Symbol.iterator]||e[`@@iterator`];if(n!=null){var r,i,a,o,s=[],c=!0,l=!1;try{if(a=(n=n.call(e)).next,t===0){if(Object(n)!==n)return;c=!1}else for(;!(c=(r=a.call(n)).done)&&(s.push(r.value),s.length!==t);c=!0);}catch(e){l=!0,i=e}finally{try{if(!c&&n.return!=null&&(o=n.return(),Object(o)!==o))return}finally{if(l)throw i}}return s}}function _e(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}function ve(e,t){if(e){if(typeof e==`string`)return _e(e,t);var n={}.toString.call(e).slice(8,-1);return n===`Object`&&e.constructor&&(n=e.constructor.name),n===`Map`||n===`Set`?Array.from(e):n===`Arguments`||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?_e(e,t):void 0}}function ye(){return(ye=e((()=>{})))()}function be(){throw TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function xe(e,t){return he(e)||ge(e,t)||ve(e,t)||be()}function O(){return(O=e((()=>{ye()})))()}var Se=t((e=>{Object.defineProperty(e,"__esModule",{value:!0}),e.bind=void 0;function t(e,t){var n=t.type,r=t.listener,i=t.options;return e.addEventListener(n,r,i),function(){e.removeEventListener(n,r,i)}}e.bind=t})),Ce=t((e=>{var t=e&&e.__assign||function(){return t=Object.assign||function(e){for(var t,n=1,r=arguments.length;n<r;n++)for(var i in t=arguments[n],t)Object.prototype.hasOwnProperty.call(t,i)&&(e[i]=t[i]);return e},t.apply(this,arguments)};Object.defineProperty(e,"__esModule",{value:!0}),e.bindAll=void 0;var n=Se();function r(e){if(e!==void 0)return typeof e==`boolean`?{capture:e}:e}function i(e,n){return n==null?e:t(t({},e),{options:t(t({},r(n)),r(e.options))})}function a(e,t,r){var a=t.map(function(t){var a=i(t,r);return(0,n.bind)(e,a)});return function(){a.forEach(function(e){return e()})}}e.bindAll=a})),k=t((e=>{Object.defineProperty(e,"__esModule",{value:!0}),e.bindAll=e.bind=void 0;var t=Se();Object.defineProperty(e,"bind",{enumerable:!0,get:function(){return t.bind}});var n=Ce();Object.defineProperty(e,"bindAll",{enumerable:!0,get:function(){return n.bindAll}})})),we;function Te(){return(Te=e((()=>{we=`data-pdnd-honey-pot`})))()}function Ee(e){return e instanceof Element&&e.hasAttribute(`data-pdnd-honey-pot`)}function De(){return(De=e((()=>{Te()})))()}function Oe(e){var t=xe(document.elementsFromPoint(e.x,e.y),2),n=t[0],r=t[1];return n?Ee(n)?r??null:n:null}function ke(){return(ke=e((()=>{O(),De()})))()}function A(e){"@babel/helpers - typeof";return A=typeof Symbol==`function`&&typeof Symbol.iterator==`symbol`?function(e){return typeof e}:function(e){return e&&typeof Symbol==`function`&&e.constructor===Symbol&&e!==Symbol.prototype?`symbol`:typeof e},A(e)}function Ae(e,t){if(A(e)!=`object`||!e)return e;var n=e[Symbol.toPrimitive];if(n!==void 0){var r=n.call(e,t||`default`);if(A(r)!=`object`)return r;throw TypeError(`@@toPrimitive must return a primitive value.`)}return(t===`string`?String:Number)(e)}function je(){return(je=e((()=>{})))()}function Me(e){var t=Ae(e,`string`);return A(t)==`symbol`?t:t+``}function Ne(){return(Ne=e((()=>{je()})))()}function j(e,t,n){return(t=Me(t))in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function M(){return(M=e((()=>{Ne()})))()}var Pe;function Fe(){return(Fe=e((()=>{Pe=2147483647})))()}var Ie;function Le(){return(Le=e((()=>{Ie={inset:`unset`,border:`none`,padding:0,margin:0,overflow:`visible`,color:`inherit`,background:`transparent`,width:`auto`,height:`auto`}})))()}function N(e){var t=null;return function(){if(!t){var n=[...arguments];t={result:e.apply(this,n)}}return t.result}}var P;function Re(){return(Re=e((()=>{P=N(function(){return typeof HTMLElement<`u`&&typeof HTMLElement.prototype.showPopover==`function`})})))()}function ze(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function Be(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?ze(Object(n),!0).forEach(function(t){j(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):ze(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function Ve(e){return{x:Math.floor(e.x),y:Math.floor(e.y)}}function He(e){return{x:e.x-Xe,y:e.y-Xe}}function Ue(e){return{x:Math.max(e.x,0),y:Math.max(e.y,0)}}function We(e){return{x:Math.min(e.x,window.innerWidth-I),y:Math.min(e.y,window.innerHeight-I)}}function Ge(e){var t=e.client,n=We(Ue(He(Ve(t))));return DOMRect.fromRect({x:n.x,y:n.y,width:I,height:I})}function Ke(e){var t=e.clientRect;return{left:`${t.left}px`,top:`${t.top}px`,width:`${t.width}px`,height:`${t.height}px`}}function qe(e){var t=e.client,n=e.clientRect;return t.x>=n.x&&t.x<=n.x+n.width&&t.y>=n.y&&t.y<=n.y+n.height}function Je(e){var t=e.initial,n=document.createElement(`div`);n.setAttribute(we,`true`),P()&&n.setAttribute(`popover`,`manual`);var r=Ge({client:t});Object.assign(n.style,Be(Be({position:`fixed`},P()?Ie:{zIndex:Pe}),{},{backgroundColor:`transparent`,padding:0,margin:0,boxSizing:`border-box`,pointerEvents:`auto`},Ke({clientRect:r}))),document.body.appendChild(n),P()&&n.showPopover();var i=(0,F.bind)(window,{type:`pointermove`,listener:function(e){r=Ge({client:{x:e.clientX,y:e.clientY}}),Object.assign(n.style,Ke({clientRect:r}))},options:{capture:!0}});return function(e){var t=e.current;if(i(),qe({client:t,clientRect:r})){n.remove();return}function a(){o(),n.remove()}var o=(0,F.bindAll)(window,[{type:`pointerdown`,listener:a},{type:`pointermove`,listener:a},{type:`focusin`,listener:a},{type:`focusout`,listener:a},{type:`dragstart`,listener:a},{type:`dragenter`,listener:a},{type:`dragover`,listener:a}],{capture:!0})}}function Ye(){var e=null;function t(){return e=null,(0,F.bind)(window,{type:`pointermove`,listener:function(t){e={x:t.clientX,y:t.clientY}},options:{capture:!0}})}function n(){var t=null;return function(n){var r=n.eventName,i=n.payload;if(r===`onDragStart`){var a=i.location.initial.input;t=Je({initial:e??{x:a.clientX,y:a.clientY}})}if(r===`onDrop`){var o,s=i.location.current.input;(o=t)==null||o({current:{x:s.clientX,y:s.clientY}}),t=null,e=null}}}return{bindEvents:t,getOnPostDispatch:n}}var F,I,Xe;function Ze(){return(Ze=e((()=>{M(),F=k(),Fe(),Le(),Re(),Te(),I=2,Xe=I/2})))()}function Qe(e){if(Array.isArray(e))return _e(e)}function $e(){return($e=e((()=>{})))()}function et(e){if(typeof Symbol<`u`&&e[Symbol.iterator]!=null||e[`@@iterator`]!=null)return Array.from(e)}function tt(){throw TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function nt(e){return Qe(e)||et(e)||ve(e)||tt()}function rt(){return(rt=e((()=>{$e(),ye()})))()}var it;function at(){return(at=e((()=>{it=N(function(){return navigator.userAgent.includes(`Firefox`)})})))()}var L;function ot(){return(ot=e((()=>{L=N(function(){var e=navigator.userAgent;return e.includes(`AppleWebKit`)&&!e.includes(`Chrome`)})})))()}function st(e){var t=e.dragLeave;return L()?t.hasOwnProperty(R.isLeavingWindow):!1}var ct,R;function lt(){return(lt=e((()=>{ct=k(),ot(),R={isLeavingWindow:Symbol(`leaving`),isEnteringWindow:Symbol(`entering`)},(function(){if(typeof window>`u`||!L())return;function e(){return{enterCount:0,isOverWindow:!1}}var t=e();function n(){t=e()}(0,ct.bindAll)(window,[{type:`dragstart`,listener:function(){t.enterCount=0,t.isOverWindow=!0}},{type:`drop`,listener:n},{type:`dragend`,listener:n},{type:`dragenter`,listener:function(e){!t.isOverWindow&&t.enterCount===0&&(e[R.isEnteringWindow]=!0),t.isOverWindow=!0,t.enterCount++}},{type:`dragleave`,listener:function(e){t.enterCount--,t.isOverWindow&&t.enterCount===0&&(e[R.isLeavingWindow]=!0,t.isOverWindow=!1)}}],{capture:!0})})()})))()}function ut(e){return`nodeName`in e}function dt(e){return ut(e)&&e.ownerDocument!==document}function ft(e){var t=e.dragLeave,n=t.type,r=t.relatedTarget;return n===`dragleave`?L()?st({dragLeave:t}):r==null?!0:it()?dt(r):r instanceof HTMLIFrameElement:!1}function pt(){return(pt=e((()=>{at(),ot(),lt()})))()}function mt(e){var t=e.onDragEnd;return[{type:`pointermove`,listener:function(){var e=0;return function(){if(e<20){e++;return}t()}}()},{type:`pointerdown`,listener:t}]}function z(e){return{altKey:e.altKey,button:e.button,buttons:e.buttons,ctrlKey:e.ctrlKey,metaKey:e.metaKey,shiftKey:e.shiftKey,clientX:e.clientX,clientY:e.clientY,pageX:e.pageX,pageY:e.pageY}}var ht;function gt(){return(gt=e((()=>{ht=function(e){var t=[],n=null,r=function(){t=[...arguments],!n&&(n=requestAnimationFrame(function(){n=null,e.apply(void 0,t)}))};return r.cancel=function(){n&&=(cancelAnimationFrame(n),null)},r}})))()}function _t(e){var t=e.source,n=e.initial,r=e.dispatchEvent,i={dropTargets:[]};function a(e){r(e),i={dropTargets:e.payload.location.current.dropTargets}}return{start:function(e){var r=e.nativeSetDragImage,o={current:n,previous:i,initial:n};a({eventName:`onGenerateDragPreview`,payload:{source:t,location:o,nativeSetDragImage:r}}),V.schedule(function(){a({eventName:`onDragStart`,payload:{source:t,location:o}})})},dragUpdate:function(e){var r=e.current;V.flush(),B.cancel(),a({eventName:`onDropTargetChange`,payload:{source:t,location:{initial:n,previous:i,current:r}}})},drag:function(e){var r=e.current;B(function(){V.flush(),a({eventName:`onDrag`,payload:{source:t,location:{initial:n,previous:i,current:r}}})})},drop:function(e){var r=e.current,o=e.updatedSourcePayload;V.flush(),B.cancel(),a({eventName:`onDrop`,payload:{source:o??t,location:{current:r,previous:i,initial:n}}})}}}var B,V;function vt(){return(vt=e((()=>{gt(),B=ht(function(e){return e()}),V=function(){var e=null;function t(t){e={frameId:requestAnimationFrame(function(){e=null,t()}),fn:t}}function n(){e&&=(cancelAnimationFrame(e.frameId),e.fn(),null)}return{schedule:t,flush:n}}()})))()}function yt(){return!H.isActive}function bt(e){return e.dataTransfer?e.dataTransfer.setDragImage.bind(e.dataTransfer):null}function xt(e){var t=e.current,n=e.next;if(t.length!==n.length)return!0;for(var r=0;r<t.length;r++)if(t[r].element!==n[r].element)return!0;return!1}function St(e){var t=e.event,n=e.dragType,r=e.getDropTargetsOver,i=e.dispatchEvent;if(!yt())return;var a=wt({event:t,dragType:n,getDropTargetsOver:r});H.isActive=!0;var o={current:a};Ct({event:t,current:a.dropTargets});var s=_t({source:n.payload,dispatchEvent:i,initial:a});function c(e){var t=xt({current:o.current.dropTargets,next:e.dropTargets});o.current=e,t&&s.dragUpdate({current:o.current})}function l(e){var t=z(e),i=r({target:Ee(e.target)?Oe({x:t.clientX,y:t.clientY}):e.target,input:t,source:n.payload,current:o.current.dropTargets});i.length&&(e.preventDefault(),Ct({event:e,current:i})),c({dropTargets:i,input:t})}function u(){o.current.dropTargets.length&&c({dropTargets:[],input:o.current.input}),s.drop({current:o.current,updatedSourcePayload:null}),d()}function d(){H.isActive=!1,f()}var f=(0,Tt.bindAll)(window,[{type:`dragover`,listener:function(e){l(e),s.drag({current:o.current})}},{type:`dragenter`,listener:l},{type:`dragleave`,listener:function(e){ft({dragLeave:e})&&(c({input:o.current.input,dropTargets:[]}),n.startedFrom===`external`&&u())}},{type:`drop`,listener:function(e){if(o.current={dropTargets:o.current.dropTargets,input:z(e)},!o.current.dropTargets.length){u();return}e.preventDefault(),Ct({event:e,current:o.current.dropTargets}),s.drop({current:o.current,updatedSourcePayload:n.type===`external`?n.getDropPayload(e):null}),d()}},{type:`dragend`,listener:function(e){o.current={dropTargets:o.current.dropTargets,input:z(e)},u()}}].concat(nt(mt({onDragEnd:u}))),{capture:!0});s.start({nativeSetDragImage:bt(t)})}function Ct(e){var t=e.event,n=e.current[0]?.dropEffect;n!=null&&t.dataTransfer&&(t.dataTransfer.dropEffect=n)}function wt(e){var t=e.event,n=e.dragType,r=e.getDropTargetsOver,i=z(t);return n.startedFrom===`external`?{input:i,dropTargets:[]}:{input:i,dropTargets:r({input:i,source:n.payload,target:t.target,current:[]})}}var Tt,H,U;function Et(){return(Et=e((()=>{rt(),Tt=k(),ke(),De(),pt(),vt(),H={isActive:!1},U={canStart:yt,start:St}})))()}function Dt(e){var t=e.typeKey,n=e.mount,r=W.get(t);if(r)return r.usageCount++,r;var i={typeKey:t,unmount:n(),usageCount:1};return W.set(t,i),i}function Ot(e){var t=Dt(e);return function(){t.usageCount--,!(t.usageCount>0)&&(t.unmount(),W.delete(e.typeKey))}}var W;function kt(){return(kt=e((()=>{W=new Map})))()}function At(){var e=[...arguments];return function(){e.forEach(function(e){return e()})}}function jt(e,t){var n=t.attribute,r=t.value;return e.setAttribute(n,r),function(){return e.removeAttribute(n)}}function Mt(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function G(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?Mt(Object(n),!0).forEach(function(t){j(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):Mt(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function Nt(e,t){var n=typeof Symbol<`u`&&e[Symbol.iterator]||e[`@@iterator`];if(!n){if(Array.isArray(e)||(n=Pt(e))||t&&e&&typeof e.length==`number`){n&&(e=n);var r=0,i=function(){};return{s:i,n:function(){return r>=e.length?{done:!0}:{done:!1,value:e[r++]}},e:function(e){throw e},f:i}}throw TypeError(`Invalid attempt to iterate non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var a,o=!0,s=!1;return{s:function(){n=n.call(e)},n:function(){var e=n.next();return o=e.done,e},e:function(e){s=!0,a=e},f:function(){try{o||n.return==null||n.return()}finally{if(s)throw a}}}}function Pt(e,t){if(e){if(typeof e==`string`)return Ft(e,t);var n={}.toString.call(e).slice(8,-1);return n===`Object`&&e.constructor&&(n=e.constructor.name),n===`Map`||n===`Set`?Array.from(e):n===`Arguments`||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?Ft(e,t):void 0}}function Ft(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}function It(e){return e.slice(0).reverse()}function Lt(e){var t=e.typeKey,n=e.defaultDropEffect,r=new WeakMap,i=`data-drop-target-for-${t}`,a=`[${i}]`;function o(e){return r.set(e.element,e),function(){return r.delete(e.element)}}function s(e){return N(At(jt(e.element,{attribute:i,value:`true`}),o(e)))}function c(e){var t=e.source,i=e.target,o=e.input,s=e.result,l=s===void 0?[]:s;if(i==null)return l;if(!(i instanceof Element))return i instanceof Node?c({source:t,target:i.parentElement,input:o,result:l}):l;var u=i.closest(a);if(u==null)return l;var d=r.get(u);if(d==null)return l;var f={input:o,source:t,element:d.element};if(d.canDrop&&!d.canDrop(f))return c({source:t,target:d.element.parentElement,input:o,result:l});var p=d.getData?.call(d,f)??{},m=d.getDropEffect?.call(d,f)??n,h={data:p,element:d.element,dropEffect:m,isActiveDueToStickiness:!1};return c({source:t,target:d.element.parentElement,input:o,result:[].concat(nt(l),[h])})}function l(e){var t=e.eventName,n=e.payload,i=Nt(n.location.current.dropTargets),a;try{for(i.s();!(a=i.n()).done;){var o,s=a.value,c=r.get(s.element),l=G(G({},n),{},{self:s});c==null||(o=c[t])==null||o.call(c,l)}}catch(e){i.e(e)}finally{i.f()}}var u={onGenerateDragPreview:l,onDrag:l,onDragStart:l,onDrop:l,onDropTargetChange:function(e){var t=e.payload,n=new Set(t.location.current.dropTargets.map(function(e){return e.element})),i=new Set,a=Nt(t.location.previous.dropTargets),o;try{for(a.s();!(o=a.n()).done;){var s,c=o.value;i.add(c.element);var l=r.get(c.element),u=n.has(c.element),d=G(G({},t),{},{self:c});if(l==null||(s=l.onDropTargetChange)==null||s.call(l,d),!u){var f;l==null||(f=l.onDragLeave)==null||f.call(l,d)}}}catch(e){a.e(e)}finally{a.f()}var p=Nt(t.location.current.dropTargets),m;try{for(p.s();!(m=p.n()).done;){var h,g,_=m.value;if(!i.has(_.element)){var v=G(G({},t),{},{self:_}),y=r.get(_.element);y==null||(h=y.onDropTargetChange)==null||h.call(y,v),y==null||(g=y.onDragEnter)==null||g.call(y,v)}}}catch(e){p.e(e)}finally{p.f()}}};function d(e){u[e.eventName](e)}function f(e){var t=e.source,n=e.target,i=e.input,a=e.current,o=c({source:t,target:n,input:i});if(o.length>=a.length)return o;for(var s=It(a),l=It(o),u=[],d=0;d<s.length;d++){var f,p=s[d],m=l[d];if(m!=null){u.push(m);continue}var h=u[d-1],g=s[d-1];if(h?.element!==g?.element)break;var _=r.get(p.element);if(!_)break;var v={input:i,source:t,element:_.element};if(_.canDrop&&!_.canDrop(v)||!((f=_.getIsSticky)!=null&&f.call(_,v)))break;u.push(G(G({},p),{},{isActiveDueToStickiness:!0}))}return It(u)}return{dropTargetForConsumers:s,getIsOver:f,dispatchEvent:d}}function Rt(){return(Rt=e((()=>{M(),rt()})))()}function zt(e,t){var n=typeof Symbol<`u`&&e[Symbol.iterator]||e[`@@iterator`];if(!n){if(Array.isArray(e)||(n=Bt(e))||t&&e&&typeof e.length==`number`){n&&(e=n);var r=0,i=function(){};return{s:i,n:function(){return r>=e.length?{done:!0}:{done:!1,value:e[r++]}},e:function(e){throw e},f:i}}throw TypeError(`Invalid attempt to iterate non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var a,o=!0,s=!1;return{s:function(){n=n.call(e)},n:function(){var e=n.next();return o=e.done,e},e:function(e){s=!0,a=e},f:function(){try{o||n.return==null||n.return()}finally{if(s)throw a}}}}function Bt(e,t){if(e){if(typeof e==`string`)return Vt(e,t);var n={}.toString.call(e).slice(8,-1);return n===`Object`&&e.constructor&&(n=e.constructor.name),n===`Map`||n===`Set`?Array.from(e):n===`Arguments`||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?Vt(e,t):void 0}}function Vt(e,t){(t==null||t>e.length)&&(t=e.length);for(var n=0,r=Array(t);n<t;n++)r[n]=e[n];return r}function Ht(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function Ut(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?Ht(Object(n),!0).forEach(function(t){j(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):Ht(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function Wt(){var e=new Set,t=null;function n(e){t&&(!e.canMonitor||e.canMonitor(t.canMonitorArgs))&&t.active.add(e)}function r(r){var i=Ut({},r);e.add(i),n(i);function a(){e.delete(i),t&&t.active.delete(i)}return N(a)}function i(r){var i=r.eventName,a=r.payload;if(i===`onGenerateDragPreview`){t={canMonitorArgs:{initial:a.location.initial,source:a.source},active:new Set};var o=zt(e),s;try{for(o.s();!(s=o.n()).done;){var c=s.value;n(c)}}catch(e){o.e(e)}finally{o.f()}}if(t){for(var l=Array.from(t.active),u=0,d=l;u<d.length;u++){var f=d[u];if(t.active.has(f)){var p;(p=f[i])==null||p.call(f,a)}}i===`onDrop`&&(t.active.clear(),t=null)}}return{dispatchEvent:i,monitorForConsumers:r}}function Gt(){return(Gt=e((()=>{M()})))()}function Kt(e){var t=e.typeKey,n=e.mount,r=e.dispatchEventToSource,i=e.onPostDispatch,a=e.defaultDropEffect,o=Wt(),s=Lt({typeKey:t,defaultDropEffect:a});function c(e){r?.(e),s.dispatchEvent(e),o.dispatchEvent(e),i?.(e)}function l(e){var t=e.event,n=e.dragType;U.start({event:t,dragType:n,getDropTargetsOver:s.getIsOver,dispatchEvent:c})}function u(){function e(){return n({canStart:U.canStart,start:l})}return Ot({typeKey:t,mount:e})}return{registerUsage:u,dropTarget:s.dropTargetForConsumers,monitor:o.monitorForConsumers}}function qt(){return(qt=e((()=>{Et(),kt(),Rt(),Gt()})))()}var Jt,Yt;function Xt(){return(Xt=e((()=>{Jt=N(function(){return navigator.userAgent.toLocaleLowerCase().includes(`android`)}),Yt=`pdnd:android-fallback`})))()}var Zt;function Qt(){return(Qt=e((()=>{Zt=`text/plain`})))()}function $t(){return($t=e((()=>{})))()}var en;function tn(){return(tn=e((()=>{en=`application/vnd.pdnd`})))()}function nn(e){return K.set(e.element,e),function(){K.delete(e.element)}}function rn(e){return N(At(q.registerUsage(),nn(e),jt(e.element,{attribute:`draggable`,value:`true`})))}var an,K,on,q,sn,cn;function ln(){return(ln=e((()=>{O(),an=k(),ke(),Ze(),qt(),Xt(),Qt(),$t(),tn(),K=new WeakMap,on=Ye(),q=Kt({typeKey:`element`,defaultDropEffect:`move`,mount:function(e){return At(on.bindEvents(),(0,an.bind)(document,{type:`dragstart`,listener:function(t){if(e.canStart(t)&&!t.defaultPrevented&&t.dataTransfer){var n=t.target;if(n instanceof HTMLElement){var r=K.get(n);if(r){var i=z(t),a={element:r.element,dragHandle:r.dragHandle??null,input:i};if(r.canDrag&&!r.canDrag(a)){t.preventDefault();return}if(r.dragHandle){var o=Oe({x:i.clientX,y:i.clientY});if(!r.dragHandle.contains(o)){t.preventDefault();return}}var s=r.getInitialDataForExternal?.call(r,a)??null;if(s)for(var c=0,l=Object.entries(s);c<l.length;c++){var u=xe(l[c],2),d=u[0],f=u[1];t.dataTransfer.setData(d,f??``)}Jt()&&!t.dataTransfer.types.includes(`text/plain`)&&!t.dataTransfer.types.includes(`text/uri-list`)&&t.dataTransfer.setData(Zt,Yt),t.dataTransfer.setData(en,``);var p={type:`element`,payload:{element:r.element,dragHandle:r.dragHandle??null,data:r.getInitialData?.call(r,a)??{}},startedFrom:`internal`};e.start({event:t,dragType:p})}}}}}))},dispatchEventToSource:function(e){var t,n,r=e.eventName,i=e.payload;(t=K.get(i.source.element))==null||(n=t[r])==null||n.call(t,i)},onPostDispatch:on.getOnPostDispatch()}),sn=q.dropTarget,cn=q.monitor})))()}function J(){return(J=e((()=>{ln()})))()}function un(e){var t=e.list,n=e.startIndex,r=e.finishIndex;if(n===-1||r===-1)return Array.from(t);var i=Array.from(t),a=xe(i.splice(n,1),1)[0];return i.splice(r,0,a),i}function dn(){return(dn=e((()=>{O()})))()}function fn(e){let t=v(!1),r=e.enabled??v(!0);return n([e.element,()=>e.dragHandle?.value,r],([n,r,i],a,o)=>{!n||!i||o(rn({element:n,dragHandle:r??void 0,canDrag:e.canDrag,getInitialData:e.getInitialData,onDragStart:()=>{t.value=!0},onDrop:()=>{t.value=!1}}))},{flush:`post`,immediate:!0}),{isDragging:t}}var pn;function mn(){return(mn=e((()=>{J(),_(),pn=`csp-sortable-item`})))()}function hn(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),n.push.apply(n,r)}return n}function gn(e){for(var t=1;t<arguments.length;t++){var n=arguments[t]==null?{}:arguments[t];t%2?hn(Object(n),!0).forEach(function(t){j(e,t,n[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):hn(Object(n)).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))})}return e}function _n(e,t){var n=t.element,r=t.input,i=t.allowedEdges,a={x:r.clientX,y:r.clientY},o=n.getBoundingClientRect(),s=i.map(function(e){return{edge:e,value:vn[e](o,a)}}).sort(function(e,t){return e.value-t.value})[0]?.edge??null;return gn(gn({},e),{},j({},Sn,s))}var vn;function yn(){return(yn=e((()=>{M(),Y(),vn={top:function(e,t){return Math.abs(t.y-e.top)},right:function(e,t){return Math.abs(e.right-t.x)},bottom:function(e,t){return Math.abs(e.bottom-t.y)},left:function(e,t){return Math.abs(t.x-e.left)}}})))()}function bn(e){return e[Sn]??null}function xn(){return(xn=e((()=>{Y()})))()}var Sn;function Y(){return(Y=e((()=>{yn(),xn(),Sn=Symbol(`closestEdge`)})))()}function Cn(e){let t=v(!1),r=v(null),i=v(null),a=e.enabled??v(!0);return n([e.element,a],([n,a],o,s)=>{!n||!a||s(sn({element:n,canDrop:({source:t})=>!(e.canDrop&&!e.canDrop(t.data)),getData:({input:t,element:n})=>_n(e.getData({input:t,element:n}),{input:t,element:n,allowedEdges:[`top`,`bottom`]}),onDragEnter:({self:e,source:n})=>{t.value=!0,r.value=bn(e.data),i.value=typeof n.data.index==`number`?n.data.index:null},onDrag:({self:e})=>{r.value=bn(e.data)},onDragLeave:()=>{t.value=!1,r.value=null,i.value=null},onDrop:()=>{t.value=!1,r.value=null,i.value=null}}))},{flush:`post`,immediate:!0}),{isDraggedOver:t,closestEdge:r,sourceIndex:i}}function wn(){return(wn=e((()=>{Y(),J(),_()})))()}var Tn,En,Dn,On,kn,An;function jn(){return(jn=e((()=>{_(),S(),mn(),wn(),Tn={key:0,class:`csp-sortable-list-item__indicator csp-sortable-list-item__indicator--top`},En={key:2,class:`csp-sortable-list-item__handle-spacer`,"aria-hidden":`true`},Dn={class:`csp-sortable-list-item__content`},On={key:0,class:`csp-sortable-list-item__position`},kn={key:3,class:`csp-sortable-list-item__indicator csp-sortable-list-item__indicator--bottom`},An=c({__name:`CspSortableListItem`,props:{item:{},itemId:{},index:{},listId:{},draggable:{type:Boolean,default:!0},disabled:{type:Boolean,default:!1},variant:{default:`default`},showPosition:{type:Boolean,default:!1}},setup(e){let t=e,n=v(null),s=v(null),c=g(()=>!t.disabled),u=g(()=>t.draggable&&c.value);function p(){return{type:pn,listId:t.listId,itemId:t.itemId,index:t.index}}let{isDragging:m}=fn({element:n,dragHandle:s,enabled:u,getInitialData:p}),{isDraggedOver:h,sourceIndex:_}=Cn({element:n,enabled:u,canDrop:e=>e.type===`csp-sortable-item`&&e.listId===t.listId&&e.itemId!==t.itemId,getData:()=>p()}),y=g(()=>_.value!==null&&_.value<t.index),ee=g(()=>_.value!==null&&_.value>t.index),S=g(()=>h.value&&ee.value),C=g(()=>h.value&&y.value),w=g(()=>S.value?`top`:C.value?`bottom`:null);function ne(e){s.value=e}return(s,c)=>(o(),b(`li`,{ref_key:`itemRef`,ref:n,class:f([`csp-sortable-list-item`,[`csp-sortable-list-item--${e.variant}`,{"csp-sortable-list-item--dragging":d(m),"csp-sortable-list-item--drag-over":d(h)}]])},[S.value?(o(),b(`div`,Tn)):r(``,!0),u.value?(o(),b(`span`,{key:1,ref:e=>ne(e),class:`csp-sortable-list-item__handle`},[i(te,{name:`ri:draggable`,size:16})],512)):(o(),b(`span`,En)),x(`div`,Dn,[e.showPosition?(o(),b(`span`,On,l(e.index+1),1)):r(``,!0),a(s.$slots,`default`,{item:e.item,index:t.index,isDragging:d(m),isDraggedOver:d(h),closestEdge:w.value,setHandleRef:ne,isDraggable:u.value},void 0,!0)]),C.value?(o(),b(`div`,kn)):r(``,!0)],2))}})})))()}var Mn;function Nn(){return(Nn=e((()=>{jn(),C(),Mn=w(An,[[`__scopeId`,`data-v-c0741aae`]])})))()}var Pn,Fn,In,Ln,Rn;function zn(){return(zn=e((()=>{_(),me(),J(),dn(),mn(),Nn(),Pn={class:`csp-sortable-list`},Fn={key:0,class:`csp-sortable-list__header`},In={class:`csp-sortable-list__header-content`},Ln={class:`csp-sortable-list__items`},Rn=c({__name:`CspSortableList`,props:{items:{},getItemKey:{},getItemLabel:{},isItemDraggable:{},getItemVariant:{},disabled:{type:Boolean,default:!1},showPosition:{type:Boolean,default:!1}},emits:[`reorder`],setup(e,{emit:t}){let n=e,i=t,c=m();function l(e,t){return n.disabled?!1:n.isItemDraggable?.(e,t)??!0}function f(e,t){return n.getItemVariant?.(e,t)??`default`}function g(e){return n.getItemLabel?.(e)??n.getItemKey(e)}function _(e){for(let t=0;t<n.items.length;t++){let r=n.items[t];if(!l(r,t)&&n.getItemKey(e[t])!==n.getItemKey(r))return!1}return!0}function v(e,t){if(n.disabled||e===t||t<0||t>=n.items.length||!l(n.items[e],e))return;let r=un({list:n.items,startIndex:e,finishIndex:t});_(r)&&(i(`reorder`,r),fe(`${g(n.items[e])} déplacé`))}function S(e){return e<=0||!l(n.items[e],e)?!1:l(n.items[e-1],e-1)}function te(e){return e>=n.items.length-1||!l(n.items[e],e)?!1:l(n.items[e+1],e+1)}function C(e){return()=>v(e,e-1)}function w(e){return()=>v(e,e+1)}return ee(()=>cn({canMonitor:({source:e})=>e.data.type===`csp-sortable-item`&&e.data.listId===c,onDrop:({source:e,location:t})=>{if(n.disabled)return;let r=t.current.dropTargets[0];if(!r)return;let i=e.data.index,a=r.data.index;typeof i==`number`&&typeof a==`number`&&v(i,oe({startIndex:i,indexOfTarget:a,closestEdgeOfTarget:a>i?`bottom`:`top`,axis:`vertical`}))}})),(t,n)=>(o(),b(`div`,Pn,[t.$slots.header?(o(),b(`div`,Fn,[n[0]||=x(`span`,{class:`csp-sortable-list__header-handle-spacer`,"aria-hidden":`true`},null,-1),x(`div`,In,[a(t.$slots,`header`,{},void 0,!0)])])):r(``,!0),x(`ul`,Ln,[(o(!0),b(h,null,p(e.items,(n,r)=>(o(),u(Mn,{key:e.getItemKey(n),item:n,"item-id":e.getItemKey(n),index:r,"list-id":d(c),draggable:l(n,r),variant:f(n,r),disabled:e.disabled,"show-position":e.showPosition},{default:y(e=>[a(t.$slots,`item`,s({ref_for:!0},e,{canMoveUp:S(r),canMoveDown:te(r),moveUp:C(r),moveDown:w(r)}),void 0,!0)]),_:2},1032,[`item`,`item-id`,`index`,`list-id`,`draggable`,`variant`,`disabled`,`show-position`]))),128))])]))}})})))()}var X;function Bn(){return(Bn=e((()=>{zn(),C(),X=w(Rn,[[`__scopeId`,`data-v-82abd474`]])})))()}var Vn,Z,Q,$,Hn;function Un(){return(Un=e((()=>{_(),ie(),ne(),Bn(),Vn={title:`Éléments/Génériques/CspSortableList`,component:X,tags:[`autodocs`],parameters:{docs:{description:{component:"Liste réordonnable par drag and drop. Accessible via les fonctions `moveUp`/`moveDown` exposées dans le slot."}}},argTypes:{items:{control:!1,description:`Liste des éléments à afficher.`,table:{type:{summary:`T[]`}}},getItemKey:{control:!1,description:`Fonction retournant la clé unique de chaque élément.`,table:{type:{summary:`(item: T) => string`}}},getItemLabel:{control:!1,description:`Fonction retournant le libellé pour les annonces d'accessibilité.`,table:{type:{summary:`(item: T) => string`}}},isItemDraggable:{control:!1,description:`Fonction déterminant si un élément est déplaçable.`,table:{type:{summary:`(item: T, index: number) => boolean`},defaultValue:{summary:`() => true`}}},getItemVariant:{control:!1,description:`Fonction retournant la variante visuelle de chaque élément.`,table:{type:{summary:`(item: T, index: number) => 'default' | 'alt'`},defaultValue:{summary:`() => 'default'`}}},disabled:{control:{type:`boolean`},description:`Désactive le drag and drop sur toute la liste.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},onReorder:{action:`reorder`,description:`Émis quand la liste est réordonnée.`,table:{category:`Events`,type:{summary:`(items: T[]) => void`}}},item:{control:!1,description:"Slot pour personnaliser le contenu de chaque élément. Expose : `item`, `index`, `isDragging`, `isDraggable`, `canMoveUp`, `canMoveDown`, `moveUp`, `moveDown`.",table:{category:`Slots`,type:{summary:`slot`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}}},Z={render:()=>({components:{CspSortableList:X},setup(){let e=v([{id:`1`,label:`Élément 1`},{id:`2`,label:`Élément 2`},{id:`3`,label:`Élément 3`},{id:`4`,label:`Élément 4`}]);function t(t){e.value=t}return{items:e,getItemKey:e=>e.id,getItemLabel:e=>e.label,onReorder:t}},template:`
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
    `})},Q={render:()=>({components:{CspSortableList:X},setup(){let e=v([{id:`1`,label:`Élément épinglé`,pinned:!0},{id:`2`,label:`Élément 2`},{id:`3`,label:`Élément 3`},{id:`4`,label:`Élément 4`},{id:`5`,label:`Élément 5`}]);function t(t){t.findIndex(e=>e.pinned)===0&&(e.value=t)}return{items:e,getItemKey:e=>e.id,getItemLabel:e=>e.label,isItemDraggable:e=>!e.pinned,getItemVariant:e=>e.pinned?`alt`:`default`,onReorder:t}},template:`
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
    `})},$={render:()=>({components:{CspSortableList:X,CspButton:ae,CspDropdownMenu:re},setup(){let e=v([{id:`1`,label:`Élément 1`},{id:`2`,label:`Élément 2`},{id:`3`,label:`Élément 3`},{id:`4`,label:`Élément 4`}]);function t(t){e.value=t}function n(t){e.value=e.value.filter(e=>e.id!==t)}function r(e,t,r,i,a){return[{items:[{label:`Monter`,icon:`ri:arrow-up-s-line`,disabled:!e,onSelect:r},{label:`Descendre`,icon:`ri:arrow-down-s-line`,disabled:!t,onSelect:i}]},{items:[{label:`Supprimer`,icon:`ri:delete-bin-line`,destructive:!0,onSelect:()=>n(a)}]}]}return{items:e,getItemKey:e=>e.id,getItemLabel:e=>e.label,onReorder:t,getMenuSections:r}},template:`
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