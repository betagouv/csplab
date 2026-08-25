import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,C as n,D as r,Dt as i,E as a,Et as o,F as s,J as c,Q as l,R as u,S as d,T as f,Tt as p,U as m,V as h,W as g,Z as _,_ as v,b as y,c as b,dt as x,g as S,k as C,m as ee,mt as w,nt as T,vt as E,x as D,xt as O,y as k,z as te}from"./iframe-CeeHVG9Q.js";import{n as A,t as j}from"./CspIcon-CWFxm5uc.js";import{C as M,E as N,T as P,_ as ne,a as re,d as ie,g as F,i as I,l as ae,n as L,o as oe,t as R}from"./useForwardExpose-D7zAat2Q.js";import{t as se}from"./getActiveElement-D008H-Sb.js";import{n as z,t as B}from"./Primitive-Qnm6bco1.js";import{n as ce,t as le}from"./Presence-BdAdyWfC.js";import{a as ue,i as de,n as fe,t as pe}from"./Teleport-enlKnAiU.js";import{a as me,c as he,o as ge}from"./utils-B16bEgo_.js";import{n as _e,t as V}from"./Collection-Db_4UVi4.js";import{n as ve,t as ye}from"./VisuallyHidden-01y3F0iV.js";import{n as be,t as H}from"./CspButton-DNaFuWNd.js";var xe;function Se(){return(Se=e((()=>{R(),z(),ue(),b(),xe=r({__name:`DismissableLayerBranch`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){let t=e,{forwardRef:n,currentElement:r}=L();return u(()=>{de.branches.add(r.value)}),te(()=>{de.branches.delete(r.value)}),(e,r)=>(h(),D(O(B),s({ref:O(n)},t),{default:T(()=>[g(e.$slots,`default`)]),_:3},16))}})})))()}var U;function Ce(){return(Ce=e((()=>{z(),b(),U=r({__name:`ToastAnnounceExclude`,props:{altText:{type:String,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){return(e,t)=>(h(),D(O(B),{as:e.as,"as-child":e.asChild,"data-reka-toast-announce-exclude":``,"data-reka-toast-announce-alt":e.altText||void 0},{default:T(()=>[g(e.$slots,`default`)]),_:3},8,[`as`,`as-child`,`data-reka-toast-announce-alt`]))}})})))()}var W,we,Te;function G(){return(G=e((()=>{N(),V(),b(),[W,we]=P(`ToastProvider`),Te=r({inheritAttrs:!1,__name:`ToastProvider`,props:{label:{type:String,required:!1,default:`Notification`},duration:{type:Number,required:!1,default:5e3},disableSwipe:{type:Boolean,required:!1},swipeDirection:{type:String,required:!1,default:`right`},swipeThreshold:{type:Number,required:!1,default:50}},setup(e){let t=e,{label:n,duration:r,disableSwipe:i,swipeDirection:a,swipeThreshold:o}=E(t);_e({isProvider:!0});let s=w(),c=w(0),l=w(!1),u=w(!1);if(t.label&&typeof t.label==`string`&&!t.label.trim())throw Error("Invalid prop `label` supplied to `ToastProvider`. Expected non-empty `string`.");return we({label:n,duration:r,disableSwipe:i,swipeDirection:a,swipeThreshold:o,toastCount:c,viewport:s,onViewportChange(e){s.value=e},onToastAdd(){c.value++},onToastRemove(){c.value--},isFocusedToastEscapeKeyDownRef:l,isClosePausedRef:u}),(e,t)=>g(e.$slots,`default`)}})})))()}var Ee;function De(){return(De=e((()=>{ve(),G(),b(),F(),Ee=r({__name:`ToastAnnounce`,setup(e){let t=W(),n=M(1e3),r=w(!1),a=0,o=0;return ne&&(a=requestAnimationFrame(()=>{o=requestAnimationFrame(()=>{r.value=!0})}),x(()=>{cancelAnimationFrame(a),cancelAnimationFrame(o)})),(e,a)=>O(n)||r.value?(h(),D(O(ye),{key:0,feature:`fully-hidden`},{default:T(()=>[f(i(O(t).label.value)+` `,1),g(e.$slots,`default`)]),_:3})):d(`v-if`,!0)}})})))()}function K(e,t,n){let r=n.originalEvent.currentTarget,i=new CustomEvent(e,{bubbles:!1,cancelable:!0,detail:n});t&&r.addEventListener(e,t,{once:!0}),r.dispatchEvent(i)}function Oe(e,t,n=0){let r=Math.abs(e.x),i=Math.abs(e.y),a=r>i;return t===`left`||t===`right`?a&&r>n:!a&&i>n}function ke(e){return e.nodeType===e.ELEMENT_NODE}function Ae(e){let t=[];return Array.from(e.childNodes).forEach(e=>{if(e.nodeType===e.TEXT_NODE&&e.textContent&&t.push(e.textContent),ke(e)){let n=e.ariaHidden||e.hidden||e.style.display===`none`,r=e.dataset.rekaToastAnnounceExclude===``;if(!n){if(r){let n=e.dataset.rekaToastAnnounceAlt;n&&t.push(n)}else t.push(...Ae(e))}}}),t}var q,J;function je(){return(je=e((()=>{q=`toast.viewportPause`,J=`toast.viewportResume`})))()}var Me,Ne,Pe;function Fe(){return(Fe=e((()=>{N(),R(),z(),V(),G(),De(),je(),b(),I(),F(),[Me,Ne]=P(`ToastRoot`),Pe=r({inheritAttrs:!1,__name:`ToastRootImpl`,props:{type:{type:String,required:!1},open:{type:Boolean,required:!1,default:!1},duration:{type:Number,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`li`}},emits:[`close`,`escapeKeyDown`,`pause`,`resume`,`swipeStart`,`swipeMove`,`swipeCancel`,`swipeEnd`],setup(e,{emit:r}){let o=e,c=r,{forwardRef:p,currentElement:_}=L(),{CollectionItem:y}=_e(),b=W(),x=w(null),C=w(null),E=k(()=>typeof o.duration==`number`?o.duration:b.duration.value),A=w(0),j=w(E.value),M=w(0),N=w(E.value),P=ae(()=>{let e=Date.now()-A.value;N.value=Math.max(j.value-e,0)},{fpsLimit:60});function ie(e){e<=0||e===1/0||ne&&(window.clearTimeout(M.value),A.value=Date.now(),M.value=window.setTimeout(F,e))}function F(e){let t=e?.pointerType===``;_.value?.contains(se())&&t&&b.viewport.value?.focus(),t&&(b.isClosePausedRef.value=!1),c(`close`)}let I=k(()=>_.value?Ae(_.value):null);if(o.type&&![`foreground`,`background`].includes(o.type))throw Error("Invalid prop `type` supplied to `Toast`. Expected `foreground | background`.");return t(e=>{let t=b.viewport.value;if(t){let e=()=>{ie(j.value),P.resume(),c(`resume`)},n=()=>{let e=Date.now()-A.value;j.value-=e,window.clearTimeout(M.value),P.pause(),c(`pause`)};return t.addEventListener(q,n),t.addEventListener(J,e),()=>{t.removeEventListener(q,n),t.removeEventListener(J,e)}}}),l(()=>[o.open,E.value],()=>{j.value=E.value,o.open&&!b.isClosePausedRef.value&&ie(E.value)},{immediate:!0}),re(`Escape`,e=>{c(`escapeKeyDown`,e),e.defaultPrevented||(b.isFocusedToastEscapeKeyDownRef.value=!0,F())}),u(()=>{b.onToastAdd()}),te(()=>{b.onToastRemove()}),Ne({onClose:F}),(e,t)=>(h(),n(S,null,[I.value?(h(),D(Ee,{key:0,role:`alert`,"aria-live":e.type===`foreground`?`assertive`:`polite`},{default:T(()=>[d(`
      Render each chunk as its own text node so screen readers get the
      natural pause break between nodes (see comment in utils.ts).
      Interpolating the array directly with \`{{ announceTextContent }}\`
      would route through Vue's \`toDisplayString\`, which JSON-stringifies
      arrays — the live region would then announce literal \`[\`, quotes
      and commas instead of the toast title and description.
    `),(h(!0),n(S,null,m(I.value,(e,t)=>(h(),n(S,{key:t},[f(i(e),1)],64))),128))]),_:1},8,[`aria-live`])):d(`v-if`,!0),O(b).viewport.value?(h(),D(v,{key:1,to:O(b).viewport.value},[a(O(y),null,{default:T(()=>[a(O(B),s({ref:O(p),tabindex:`0`},e.$attrs,{as:e.as,"as-child":e.asChild,"data-state":e.open?`open`:`closed`,"data-swipe-direction":O(b).swipeDirection.value,style:O(b).disableSwipe.value?void 0:{userSelect:`none`,touchAction:`none`},onPointerdown:t[0]||=ee(e=>{O(b).disableSwipe.value||(x.value={x:e.clientX,y:e.clientY})},[`left`]),onPointermove:t[1]||=e=>{if(O(b).disableSwipe.value||!x.value)return;let t=e.clientX-x.value.x,n=e.clientY-x.value.y,r=!!C.value,i=[`left`,`right`].includes(O(b).swipeDirection.value),a=[`left`,`up`].includes(O(b).swipeDirection.value)?Math.min:Math.max,o=i?a(0,t):0,s=i?0:a(0,n),l=e.pointerType===`touch`?10:2,u={x:o,y:s},d={originalEvent:e,delta:u};r?(C.value=u,O(K)(O(`toast.swipeMove`),e=>c(`swipeMove`,e),d)):O(Oe)(u,O(b).swipeDirection.value,l)?(C.value=u,O(K)(O(`toast.swipeStart`),e=>c(`swipeStart`,e),d),e.target.setPointerCapture(e.pointerId)):(Math.abs(t)>l||Math.abs(n)>l)&&(x.value=null)},onPointerup:t[2]||=e=>{if(O(b).disableSwipe.value)return;let t=C.value,n=e.target;if(n.hasPointerCapture(e.pointerId)&&n.releasePointerCapture(e.pointerId),C.value=null,x.value=null,t){let n=e.currentTarget,r={originalEvent:e,delta:t};O(Oe)(t,O(b).swipeDirection.value,O(b).swipeThreshold.value)?O(K)(O(`toast.swipeEnd`),e=>c(`swipeEnd`,e),r):O(K)(O(`toast.swipeCancel`),e=>c(`swipeCancel`,e),r),n?.addEventListener(`click`,e=>e.preventDefault(),{once:!0})}}}),{default:T(()=>[g(e.$slots,`default`,{remaining:N.value,duration:E.value})]),_:3},16,[`as`,`as-child`,`data-state`,`data-swipe-direction`,`style`])]),_:3})],8,[`to`])):d(`v-if`,!0)],64))}})})))()}var Ie;function Le(){return(Le=e((()=>{R(),z(),Ce(),Fe(),b(),Ie=r({__name:`ToastClose`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`button`}},setup(e){let t=e,n=Me(),{forwardRef:r}=L();return(e,i)=>(h(),D(U,{"as-child":``},{default:T(()=>[a(O(B),s(t,{ref:O(r),type:e.as===`button`?`button`:void 0,onClick:O(n).onClose}),{default:T(()=>[g(e.$slots,`default`)]),_:3},16,[`type`,`onClick`])]),_:3}))}})})))()}var Re;function ze(){return(ze=e((()=>{R(),Ce(),Le(),b(),Re=r({__name:`ToastAction`,props:{altText:{type:String,required:!0},asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){if(!e.altText)throw Error("Missing prop `altText` expected on `ToastAction`");let{forwardRef:t}=L();return(e,n)=>e.altText?(h(),D(U,{key:0,"alt-text":e.altText,"as-child":``},{default:T(()=>[a(Ie,{ref:O(t),as:e.as,"as-child":e.asChild},{default:T(()=>[g(e.$slots,`default`)]),_:3},8,[`as`,`as-child`])]),_:3},8,[`alt-text`])):d(`v-if`,!0)}})})))()}var Be;function Ve(){return(Ve=e((()=>{R(),z(),b(),Be=r({__name:`ToastDescription`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){let t=e;return L(),(e,n)=>(h(),D(O(B),p(C(t)),{default:T(()=>[g(e.$slots,`default`)]),_:3},16))}})})))()}var He;function Ue(){return(Ue=e((()=>{fe(),b(),He=r({__name:`ToastPortal`,props:{to:{type:null,required:!1},disabled:{type:Boolean,required:!1},defer:{type:Boolean,required:!1},forceMount:{type:Boolean,required:!1}},setup(e){let t=e;return(e,n)=>(h(),D(O(pe),p(C(t)),{default:T(()=>[g(e.$slots,`default`)]),_:3},16))}})})))()}var We;function Ge(){return(Ge=e((()=>{R(),ce(),Fe(),b(),I(),We=r({__name:`ToastRoot`,props:{defaultOpen:{type:Boolean,required:!1,default:!0},forceMount:{type:Boolean,required:!1},type:{type:String,required:!1,default:`foreground`},open:{type:Boolean,required:!1,default:void 0},duration:{type:Number,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`li`}},emits:[`escapeKeyDown`,`pause`,`resume`,`swipeStart`,`swipeMove`,`swipeCancel`,`swipeEnd`,`update:open`],setup(e,{emit:t}){let n=e,r=t,{forwardRef:i}=L(),o=ie(n,`open`,r,{defaultValue:n.defaultOpen,passive:n.open===void 0});return(e,t)=>(h(),D(O(le),{present:e.forceMount||O(o)},{default:T(()=>[a(Pe,s({ref:O(i),open:O(o),type:e.type,as:e.as,"as-child":e.asChild,duration:e.duration},e.$attrs,{onClose:t[0]||=e=>o.value=!1,onPause:t[1]||=e=>r(`pause`),onResume:t[2]||=e=>r(`resume`),onEscapeKeyDown:t[3]||=e=>r(`escapeKeyDown`,e),onSwipeStart:t[4]||=e=>{r(`swipeStart`,e),e.defaultPrevented||e.currentTarget.setAttribute(`data-swipe`,`start`)},onSwipeMove:t[5]||=e=>{if(r(`swipeMove`,e),!e.defaultPrevented){let{x:t,y:n}=e.detail.delta,r=e.currentTarget;r.setAttribute(`data-swipe`,`move`),r.style.setProperty(`--reka-toast-swipe-move-x`,`${t}px`),r.style.setProperty(`--reka-toast-swipe-move-y`,`${n}px`)}},onSwipeCancel:t[6]||=e=>{if(r(`swipeCancel`,e),!e.defaultPrevented){let t=e.currentTarget;t.setAttribute(`data-swipe`,`cancel`),t.style.removeProperty(`--reka-toast-swipe-move-x`),t.style.removeProperty(`--reka-toast-swipe-move-y`),t.style.removeProperty(`--reka-toast-swipe-end-x`),t.style.removeProperty(`--reka-toast-swipe-end-y`)}},onSwipeEnd:t[7]||=e=>{if(r(`swipeEnd`,e),!e.defaultPrevented){let{x:t,y:n}=e.detail.delta,r=e.currentTarget;r.setAttribute(`data-swipe`,`end`),r.style.removeProperty(`--reka-toast-swipe-move-x`),r.style.removeProperty(`--reka-toast-swipe-move-y`),r.style.setProperty(`--reka-toast-swipe-end-x`,`${t}px`),r.style.setProperty(`--reka-toast-swipe-end-y`,`${n}px`),o.value=!1}}}),{default:T(({remaining:t,duration:n})=>[g(e.$slots,`default`,{remaining:t,duration:n,open:O(o)})]),_:3},16,[`open`,`type`,`as`,`as-child`,`duration`])]),_:3},8,[`present`]))}})})))()}var Ke;function qe(){return(qe=e((()=>{R(),z(),b(),Ke=r({__name:`ToastTitle`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){let t=e;return L(),(e,n)=>(h(),D(O(B),p(C(t)),{default:T(()=>[g(e.$slots,`default`)]),_:3},16))}})})))()}var Je;function Ye(){return(Ye=e((()=>{ve(),G(),b(),Je=r({__name:`FocusProxy`,emits:[`focusFromOutsideViewport`],setup(e,{emit:t}){let n=t,r=W();return(e,t)=>(h(),D(O(ye),{tabindex:`0`,style:{position:`fixed`},onFocus:t[0]||=e=>{let t=e.relatedTarget;O(r).viewport.value?.contains(t)||n(`focusFromOutsideViewport`)}},{default:T(()=>[g(e.$slots,`default`)]),_:3}))}})})))()}var Xe;function Ze(){return(Ze=e((()=>{R(),z(),Se(),he(),V(),G(),je(),Ye(),b(),I(),Xe=r({inheritAttrs:!1,__name:`ToastViewport`,props:{hotkey:{type:Array,required:!1,default:()=>[`F8`]},label:{type:[String,Function],required:!1,default:`Notifications ({hotkey})`},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`ol`}},setup(e){let{hotkey:n,label:r}=E(e),{forwardRef:i,currentElement:c}=L(),{CollectionSlot:l,getItems:f}=_e(),p=W(),m=k(()=>p.toastCount.value>0),_=w(),v=w(),y=/Key/g,b=/Digit/g,x=k(()=>n.value.join(`+`).replace(y,``).replace(b,``));re(n.value,()=>{c.value.focus()}),u(()=>{p.onViewportChange(c.value)}),t(e=>{let t=c.value;if(m.value&&t){let n=()=>{if(!p.isClosePausedRef.value){let e=new CustomEvent(q);t.dispatchEvent(e),p.isClosePausedRef.value=!0}},r=()=>{if(p.isClosePausedRef.value){let e=new CustomEvent(J);t.dispatchEvent(e),p.isClosePausedRef.value=!1}},i=e=>{t.contains(e.relatedTarget)||r()},a=()=>{t.contains(se())||r()},o=e=>{let n=e.altKey||e.ctrlKey||e.metaKey;if(e.key===`Tab`&&!n){let n=se(),r=e.shiftKey;if(e.target===t&&r){_.value?.focus();return}let i=S({tabbingDirection:r?`backwards`:`forwards`}),a=i.findIndex(e=>e===n);me(i.slice(a+1))?e.preventDefault():r?_.value?.focus():v.value?.focus()}};t.addEventListener(`focusin`,n),t.addEventListener(`focusout`,i),t.addEventListener(`pointermove`,n),t.addEventListener(`pointerleave`,a),t.addEventListener(`keydown`,o),window.addEventListener(`blur`,n),window.addEventListener(`focus`,r),e(()=>{t.removeEventListener(`focusin`,n),t.removeEventListener(`focusout`,i),t.removeEventListener(`pointermove`,n),t.removeEventListener(`pointerleave`,a),t.removeEventListener(`keydown`,o),window.removeEventListener(`blur`,n),window.removeEventListener(`focus`,r)})}});function S({tabbingDirection:e}){let t=f().map(e=>e.ref).map(t=>{let n=[t,...ge(t)];return e===`forwards`?n:n.reverse()});return(e===`forwards`?t.reverse():t).flat()}return(e,t)=>(h(),D(O(xe),{role:`region`,"aria-label":typeof O(r)==`string`?O(r).replace(`{hotkey}`,x.value):O(r)(x.value),tabindex:`-1`,style:o({pointerEvents:m.value?void 0:`none`})},{default:T(()=>[m.value?(h(),D(Je,{key:0,ref:e=>{e&&(_.value=O(oe)(e))},onFocusFromOutsideViewport:t[0]||=()=>{let e=S({tabbingDirection:`forwards`});O(me)(e)}},null,512)):d(`v-if`,!0),a(O(l),null,{default:T(()=>[a(O(B),s({ref:O(i),tabindex:`-1`,as:e.as,"as-child":e.asChild},e.$attrs),{default:T(()=>[g(e.$slots,`default`)]),_:3},16,[`as`,`as-child`])]),_:3}),m.value?(h(),D(Je,{key:1,ref:e=>{e&&(v.value=O(oe)(e))},onFocusFromOutsideViewport:t[1]||=()=>{let e=S({tabbingDirection:`backwards`});O(me)(e)}},null,512)):d(`v-if`,!0)]),_:3},8,[`aria-label`,`style`]))}})})))()}var Qe,$e,et,tt,nt,rt;function it(){return(it=e((()=>{b(),ze(),Le(),Ve(),Ge(),qe(),be(),A(),Qe={class:`csp-toast__layout`},$e={key:0,class:`csp-toast__icon`},et={class:`csp-toast__content`},tt={key:2,class:`csp-toast__body`},nt={key:1,class:`csp-toast__actions`},rt=r({inheritAttrs:!1,__name:`CspToast`,props:{open:{type:Boolean,default:void 0},defaultOpen:{type:Boolean,default:!1},title:{default:null},description:{default:null},duration:{default:void 0},variant:{default:`default`},showIcon:{type:Boolean,default:!0},actionLabel:{default:null},actionAltText:{default:`Exécuter l'action`},showClose:{type:Boolean,default:!0},closeLabel:{default:`Fermer la notification`}},emits:[`update:open`,`action`],setup(e,{emit:t}){let r=e,o=t,l=c(),u=_(),p=k(()=>!!u.title||!!r.title),m=k(()=>!!u.description||!!r.description),v=k(()=>!!u.action||!!r.actionLabel),b={default:`ri:notification-3-line`,info:`ri:information-line`,success:`ri:checkbox-circle-line`,warning:`ri:alert-line`,error:`ri:error-warning-line`},x=k(()=>b[r.variant]);return(t,r)=>(h(),D(O(We),s(O(l),{open:e.open,"default-open":e.defaultOpen,duration:e.duration,class:[`csp-toast`,`csp-toast--${e.variant}`],"onUpdate:open":r[1]||=e=>o(`update:open`,e)}),{default:T(()=>[y(`div`,Qe,[e.showIcon?(h(),n(`div`,$e,[g(t.$slots,`icon`,{},()=>[a(j,{name:x.value},null,8,[`name`])])])):d(``,!0),y(`div`,et,[p.value?(h(),D(O(Ke),{key:0,as:`h3`,class:`csp-toast__title`},{default:T(()=>[g(t.$slots,`title`,{},()=>[f(i(e.title),1)])]),_:3})):d(``,!0),m.value?(h(),D(O(Be),{key:1,as:`p`,class:`csp-toast__description`},{default:T(()=>[g(t.$slots,`description`,{},()=>[f(i(e.description),1)])]),_:3})):d(``,!0),t.$slots.default?(h(),n(`div`,tt,[g(t.$slots,`default`)])):d(``,!0)]),v.value||e.showClose?(h(),n(`div`,nt,[v.value?(h(),D(O(Re),{key:0,"as-child":``,"alt-text":e.actionAltText,onClick:r[0]||=e=>o(`action`)},{default:T(()=>[g(t.$slots,`action`,{},()=>[a(H,{variant:`tertiary-no-outline`,size:`sm`,label:e.actionLabel},null,8,[`label`])])]),_:3},8,[`alt-text`])):d(``,!0),e.showClose?(h(),D(O(Ie),{key:1,"as-child":``},{default:T(()=>[a(H,{variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":e.closeLabel},null,8,[`aria-label`])]),_:1})):d(``,!0)])):d(``,!0)])]),_:3},16,[`open`,`default-open`,`duration`,`class`]))}})})))()}var Y;function at(){return(at=e((()=>{it(),Y=rt})))()}var ot;function st(){return(st=e((()=>{b(),Ue(),G(),Ze(),ot=r({__name:`CspToastProvider`,props:{label:{default:`Notification`},duration:{default:3200},swipeDirection:{default:`right`},disableSwipe:{type:Boolean,default:!1}},setup(e){return(t,n)=>(h(),D(O(Te),{label:e.label,duration:e.duration,"disable-swipe":e.disableSwipe,"swipe-direction":e.swipeDirection},{default:T(()=>[g(t.$slots,`default`),a(O(He),null,{default:T(()=>[a(O(Xe),{class:`csp-toast-viewport`})]),_:1})]),_:3},8,[`label`,`duration`,`disable-swipe`,`swipe-direction`]))}})})))()}var X;function ct(){return(ct=e((()=>{st(),X=ot})))()}var lt,Z,Q,$,ut;function dt(){return(dt=e((()=>{b(),be(),at(),ct(),lt={title:`Éléments/Génériques/CspToast`,component:Y,tags:[`autodocs`],parameters:{controls:{include:[`open`,`defaultOpen`,`title`,`description`,`duration`,`variant`,`showIcon`,`actionLabel`,`actionAltText`,`showClose`,`closeLabel`]},docs:{description:{component:`Notification toast accessible basée sur reka-ui. Doit être utilisé à l'intérieur d'un unique CspToastProvider placé à la racine de l'app.`}}},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},defaultOpen:{control:{type:`boolean`},description:`État d'ouverture initial en mode non contrôlé.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},title:{control:{type:`text`},description:"Titre du toast (ou slot `title`).",table:{type:{summary:`string | null`}}},description:{control:{type:`text`},description:"Description du toast (ou slot `description`).",table:{type:{summary:`string | null`}}},duration:{control:{type:`number`},description:`Durée d'affichage en millisecondes. Hérite du provider si non défini.`,table:{type:{summary:`number`}}},variant:{control:{type:`radio`},options:[`default`,`info`,`success`,`warning`,`error`],description:`Variante visuelle de la notification.`,table:{type:{summary:`default | info | success | warning | error`},defaultValue:{summary:`default`}}},showIcon:{control:{type:`boolean`},description:`Affiche ou masque l'icone.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},actionLabel:{control:{type:`text`},description:`Label du bouton d'action.`,table:{type:{summary:`string | null`}}},actionAltText:{control:{type:`text`},description:`Texte alternatif annoncé pour l'action.`,table:{type:{summary:`string`},defaultValue:{summary:`Exécuter l'action`}}},showClose:{control:{type:`boolean`},description:`Affiche ou masque le bouton de fermeture.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},closeLabel:{control:{type:`text`},description:`Libellé accessible du bouton de fermeture.`,table:{type:{summary:`string`},defaultValue:{summary:`Fermer la notification`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,title:`Action terminée`,description:`Votre modification a bien été enregistrée.`,variant:`success`,showIcon:!0,actionLabel:`Annuler`,actionAltText:`Annuler la dernière action`,showClose:!0,closeLabel:`Fermer la notification`},render:e=>({components:{CspButton:H,CspToast:Y,CspToastProvider:X},setup(){let t=w(!!e.open);l(()=>e.open,e=>{e!==void 0&&(t.value=e)});function n(){t.value=!0}function r(e){t.value=e}return{args:e,open:t,showToast:n,handleUpdateOpen:r}},template:`
      <CspToastProvider>
        <CspButton
          label="Afficher le toast"
          variant="primary"
          @click="showToast"
        />

        <CspToast
          v-bind="args"
          :open="args.open === undefined ? open : args.open"
          @update:open="handleUpdateOpen"
        />
      </CspToastProvider>
    `})},Z={},Q={render:e=>({components:{CspButton:H,CspToast:Y,CspToastProvider:X},setup(){let t=[`default`,`info`,`success`,`warning`,`error`],n=w(!1),r=w(`default`);function i(e){r.value=e,n.value=!0}function a(e){n.value=e}return{args:e,variants:t,open:n,currentVariant:r,openVariant:i,updateOpen:a}},template:`
      <CspToastProvider>
        <div class="flex flex-wrap gap-3">
          <CspButton
            v-for="variant in variants"
            :key="variant"
            :label="'Toast ' + variant"
            variant="secondary"
            @click="openVariant(variant)"
          />
        </div>

        <CspToast
          v-bind="args"
          :open="open"
          :variant="currentVariant"
          :title="'Notification ' + currentVariant"
          :description="'Exemple pour la variante ' + currentVariant + '.'"
          @update:open="updateOpen"
        />
      </CspToastProvider>
    `})},$={render:()=>({components:{CspButton:H,CspToast:Y,CspToastProvider:X},setup(){let e=w([]),t=0;function n(n){e.value.push({id:t++,variant:n,title:`Notification ${n} #${t}`})}function r(t){e.value=e.value.filter(e=>e.id!==t)}return{toasts:e,addToast:n,removeToast:r}},template:`
      <CspToastProvider :duration="4000">
        <div class="flex flex-wrap gap-3">
          <CspButton label="Info" variant="secondary" @click="addToast('info')" />
          <CspButton label="Success" variant="secondary" @click="addToast('success')" />
          <CspButton label="Warning" variant="secondary" @click="addToast('warning')" />
          <CspButton label="Error" variant="secondary" @click="addToast('error')" />
        </div>

        <CspToast
          v-for="toast in toasts"
          :key="toast.id"
          :open="true"
          :variant="toast.variant"
          :title="toast.title"
          description="Cette notification fonctionne avec les autres."
          :show-close="true"
          @update:open="(v) => !v && removeToast(toast.id)"
        />
      </CspToastProvider>
    `})},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{}`,...Z.parameters?.docs?.source}}},Q.parameters={...Q.parameters,docs:{...Q.parameters?.docs,source:{originalSource:`{
  render: args => ({
    components: {
      CspButton,
      CspToast,
      CspToastProvider
    },
    setup() {
      const variants = ['default', 'info', 'success', 'warning', 'error'] as const;
      const open = ref(false);
      const currentVariant = ref<(typeof variants)[number]>('default');
      function openVariant(variant: (typeof variants)[number]) {
        currentVariant.value = variant;
        open.value = true;
      }
      function updateOpen(value: boolean) {
        open.value = value;
      }
      return {
        args,
        variants,
        open,
        currentVariant,
        openVariant,
        updateOpen
      };
    },
    template: \`
      <CspToastProvider>
        <div class="flex flex-wrap gap-3">
          <CspButton
            v-for="variant in variants"
            :key="variant"
            :label="'Toast ' + variant"
            variant="secondary"
            @click="openVariant(variant)"
          />
        </div>

        <CspToast
          v-bind="args"
          :open="open"
          :variant="currentVariant"
          :title="'Notification ' + currentVariant"
          :description="'Exemple pour la variante ' + currentVariant + '.'"
          @update:open="updateOpen"
        />
      </CspToastProvider>
    \`
  })
}`,...Q.parameters?.docs?.source}}},$.parameters={...$.parameters,docs:{...$.parameters?.docs,source:{originalSource:`{
  render: () => ({
    components: {
      CspButton,
      CspToast,
      CspToastProvider
    },
    setup() {
      const toasts = ref<Array<{
        id: number;
        variant: 'info' | 'success' | 'warning' | 'error';
        title: string;
      }>>([]);
      let nextId = 0;
      function addToast(variant: 'info' | 'success' | 'warning' | 'error') {
        toasts.value.push({
          id: nextId++,
          variant,
          title: \`Notification \${variant} #\${nextId}\`
        });
      }
      function removeToast(id: number) {
        toasts.value = toasts.value.filter(t => t.id !== id);
      }
      return {
        toasts,
        addToast,
        removeToast
      };
    },
    template: \`
      <CspToastProvider :duration="4000">
        <div class="flex flex-wrap gap-3">
          <CspButton label="Info" variant="secondary" @click="addToast('info')" />
          <CspButton label="Success" variant="secondary" @click="addToast('success')" />
          <CspButton label="Warning" variant="secondary" @click="addToast('warning')" />
          <CspButton label="Error" variant="secondary" @click="addToast('error')" />
        </div>

        <CspToast
          v-for="toast in toasts"
          :key="toast.id"
          :open="true"
          :variant="toast.variant"
          :title="toast.title"
          description="Cette notification fonctionne avec les autres."
          :show-close="true"
          @update:open="(v) => !v && removeToast(toast.id)"
        />
      </CspToastProvider>
    \`
  })
}`,...$.parameters?.docs?.source}}},ut=[`Default`,`Variants`,`MultipleToasts`]})))()}dt();export{Z as Default,$ as MultipleToasts,Q as Variants,ut as __namedExportsOrder,lt as default};