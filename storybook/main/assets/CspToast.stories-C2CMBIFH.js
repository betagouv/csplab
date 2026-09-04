import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{$ as t,A as n,B as r,C as i,D as a,Dt as o,E as s,Et as c,G as l,H as u,I as d,O as f,Ot as p,Q as m,S as h,St as g,W as _,Y as v,_ as y,b,c as x,et as ee,ft as S,h as C,ht as w,rt as T,v as te,w as E,x as D,yt as O,z as k}from"./iframe-CUXRfIIm.js";import{n as A,t as j}from"./CspIcon-CgwZss4o.js";import{C as M,E as N,T as P,_ as ne,a as re,d as F,g as I,i as L,l as ie,n as R,o as ae,t as z}from"./useForwardExpose-B8APoN_B.js";import{t as oe}from"./getActiveElement-D008H-Sb.js";import{n as B,t as V}from"./Primitive-RF66Qn_Y.js";import{n as se,t as ce}from"./Presence-CcAeiJsm.js";import{a as le,i as ue,n as de,t as fe}from"./Teleport-Arj0UvgT.js";import{a as pe,c as me,o as he}from"./utils-B16bEgo_.js";import{n as ge,t as H}from"./Collection-CqZfUwNk.js";import{n as _e,t as ve}from"./VisuallyHidden-DNzf4QpI.js";import{n as ye,t as U}from"./CspButton-CHY9EC0i.js";var be;function xe(){return(xe=e((()=>{z(),B(),le(),x(),be=f({__name:`DismissableLayerBranch`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){let t=e,{forwardRef:n,currentElement:i}=R();return k(()=>{ue.branches.add(i.value)}),r(()=>{ue.branches.delete(i.value)}),(e,r)=>(u(),h(g(V),d({ref:g(n)},t),{default:T(()=>[l(e.$slots,`default`)]),_:3},16))}})})))()}var Se;function Ce(){return(Ce=e((()=>{B(),x(),Se=f({__name:`ToastAnnounceExclude`,props:{altText:{type:String,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){return(e,t)=>(u(),h(g(V),{as:e.as,"as-child":e.asChild,"data-reka-toast-announce-exclude":``,"data-reka-toast-announce-alt":e.altText||void 0},{default:T(()=>[l(e.$slots,`default`)]),_:3},8,[`as`,`as-child`,`data-reka-toast-announce-alt`]))}})})))()}var W,we,Te;function G(){return(G=e((()=>{N(),H(),x(),[W,we]=P(`ToastProvider`),Te=f({inheritAttrs:!1,__name:`ToastProvider`,props:{label:{type:String,required:!1,default:`Notification`},duration:{type:Number,required:!1,default:5e3},disableSwipe:{type:Boolean,required:!1},swipeDirection:{type:String,required:!1,default:`right`},swipeThreshold:{type:Number,required:!1,default:50}},setup(e){let t=e,{label:n,duration:r,disableSwipe:i,swipeDirection:a,swipeThreshold:o}=O(t);ge({isProvider:!0});let s=w(),c=w(0),u=w(!1),d=w(!1);if(t.label&&typeof t.label==`string`&&!t.label.trim())throw Error("Invalid prop `label` supplied to `ToastProvider`. Expected non-empty `string`.");return we({label:n,duration:r,disableSwipe:i,swipeDirection:a,swipeThreshold:o,toastCount:c,viewport:s,onViewportChange(e){s.value=e},onToastAdd(){c.value++},onToastRemove(){c.value--},isFocusedToastEscapeKeyDownRef:u,isClosePausedRef:d}),(e,t)=>l(e.$slots,`default`)}})})))()}var Ee;function De(){return(De=e((()=>{_e(),G(),x(),I(),Ee=f({__name:`ToastAnnounce`,setup(e){let t=W(),n=M(1e3),r=w(!1),a=0,o=0;return ne&&(a=requestAnimationFrame(()=>{o=requestAnimationFrame(()=>{r.value=!0})}),S(()=>{cancelAnimationFrame(a),cancelAnimationFrame(o)})),(e,a)=>g(n)||r.value?(u(),h(g(ve),{key:0,feature:`fully-hidden`},{default:T(()=>[s(p(g(t).label.value)+` `,1),l(e.$slots,`default`)]),_:3})):i(`v-if`,!0)}})})))()}function K(e,t,n){let r=n.originalEvent.currentTarget,i=new CustomEvent(e,{bubbles:!1,cancelable:!0,detail:n});t&&r.addEventListener(e,t,{once:!0}),r.dispatchEvent(i)}function Oe(e,t,n=0){let r=Math.abs(e.x),i=Math.abs(e.y),a=r>i;return t===`left`||t===`right`?a&&r>n:!a&&i>n}function ke(e){return e.nodeType===e.ELEMENT_NODE}function Ae(e){let t=[];return Array.from(e.childNodes).forEach(e=>{if(e.nodeType===e.TEXT_NODE&&e.textContent&&t.push(e.textContent),ke(e)){let n=e.ariaHidden||e.hidden||e.style.display===`none`,r=e.dataset.rekaToastAnnounceExclude===``;if(!n){if(r){let n=e.dataset.rekaToastAnnounceAlt;n&&t.push(n)}else t.push(...Ae(e))}}}),t}var q,J;function je(){return(je=e((()=>{q=`toast.viewportPause`,J=`toast.viewportResume`})))()}var Me,Ne,Pe;function Fe(){return(Fe=e((()=>{N(),z(),B(),H(),G(),De(),je(),x(),L(),I(),[Me,Ne]=P(`ToastRoot`),Pe=f({inheritAttrs:!1,__name:`ToastRootImpl`,props:{type:{type:String,required:!1},open:{type:Boolean,required:!1,default:!1},duration:{type:Number,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`li`}},emits:[`close`,`escapeKeyDown`,`pause`,`resume`,`swipeStart`,`swipeMove`,`swipeCancel`,`swipeEnd`],setup(e,{emit:n}){let o=e,c=n,{forwardRef:f,currentElement:m}=R(),{CollectionItem:v}=ge(),x=W(),S=w(null),D=w(null),O=b(()=>typeof o.duration==`number`?o.duration:x.duration.value),A=w(0),j=w(O.value),M=w(0),N=w(O.value),P=ie(()=>{let e=Date.now()-A.value;N.value=Math.max(j.value-e,0)},{fpsLimit:60});function F(e){e<=0||e===1/0||ne&&(window.clearTimeout(M.value),A.value=Date.now(),M.value=window.setTimeout(I,e))}function I(e){let t=e?.pointerType===``;m.value?.contains(oe())&&t&&x.viewport.value?.focus(),t&&(x.isClosePausedRef.value=!1),c(`close`)}let L=b(()=>m.value?Ae(m.value):null);if(o.type&&![`foreground`,`background`].includes(o.type))throw Error("Invalid prop `type` supplied to `Toast`. Expected `foreground | background`.");return ee(e=>{let t=x.viewport.value;if(t){let e=()=>{F(j.value),P.resume(),c(`resume`)},n=()=>{let e=Date.now()-A.value;j.value-=e,window.clearTimeout(M.value),P.pause(),c(`pause`)};return t.addEventListener(q,n),t.addEventListener(J,e),()=>{t.removeEventListener(q,n),t.removeEventListener(J,e)}}}),t(()=>[o.open,O.value],()=>{j.value=O.value,o.open&&!x.isClosePausedRef.value&&F(O.value)},{immediate:!0}),re(`Escape`,e=>{c(`escapeKeyDown`,e),e.defaultPrevented||(x.isFocusedToastEscapeKeyDownRef.value=!0,I())}),k(()=>{x.onToastAdd()}),r(()=>{x.onToastRemove()}),Ne({onClose:I}),(e,t)=>(u(),E(y,null,[L.value?(u(),h(Ee,{key:0,role:`alert`,"aria-live":e.type===`foreground`?`assertive`:`polite`},{default:T(()=>[i(`
      Render each chunk as its own text node so screen readers get the
      natural pause break between nodes (see comment in utils.ts).
      Interpolating the array directly with \`{{ announceTextContent }}\`
      would route through Vue's \`toDisplayString\`, which JSON-stringifies
      arrays — the live region would then announce literal \`[\`, quotes
      and commas instead of the toast title and description.
    `),(u(!0),E(y,null,_(L.value,(e,t)=>(u(),E(y,{key:t},[s(p(e),1)],64))),128))]),_:1},8,[`aria-live`])):i(`v-if`,!0),g(x).viewport.value?(u(),h(te,{key:1,to:g(x).viewport.value},[a(g(v),null,{default:T(()=>[a(g(V),d({ref:g(f),tabindex:`0`},e.$attrs,{as:e.as,"as-child":e.asChild,"data-state":e.open?`open`:`closed`,"data-swipe-direction":g(x).swipeDirection.value,style:g(x).disableSwipe.value?void 0:{userSelect:`none`,touchAction:`none`},onPointerdown:t[0]||=C(e=>{g(x).disableSwipe.value||(S.value={x:e.clientX,y:e.clientY})},[`left`]),onPointermove:t[1]||=e=>{if(g(x).disableSwipe.value||!S.value)return;let t=e.clientX-S.value.x,n=e.clientY-S.value.y,r=!!D.value,i=[`left`,`right`].includes(g(x).swipeDirection.value),a=[`left`,`up`].includes(g(x).swipeDirection.value)?Math.min:Math.max,o=i?a(0,t):0,s=i?0:a(0,n),l=e.pointerType===`touch`?10:2,u={x:o,y:s},d={originalEvent:e,delta:u};r?(D.value=u,g(K)(g(`toast.swipeMove`),e=>c(`swipeMove`,e),d)):g(Oe)(u,g(x).swipeDirection.value,l)?(D.value=u,g(K)(g(`toast.swipeStart`),e=>c(`swipeStart`,e),d),e.target.setPointerCapture(e.pointerId)):(Math.abs(t)>l||Math.abs(n)>l)&&(S.value=null)},onPointerup:t[2]||=e=>{if(g(x).disableSwipe.value)return;let t=D.value,n=e.target;if(n.hasPointerCapture(e.pointerId)&&n.releasePointerCapture(e.pointerId),D.value=null,S.value=null,t){let n=e.currentTarget,r={originalEvent:e,delta:t};g(Oe)(t,g(x).swipeDirection.value,g(x).swipeThreshold.value)?g(K)(g(`toast.swipeEnd`),e=>c(`swipeEnd`,e),r):g(K)(g(`toast.swipeCancel`),e=>c(`swipeCancel`,e),r),n?.addEventListener(`click`,e=>e.preventDefault(),{once:!0})}}}),{default:T(()=>[l(e.$slots,`default`,{remaining:N.value,duration:O.value})]),_:3},16,[`as`,`as-child`,`data-state`,`data-swipe-direction`,`style`])]),_:3})],8,[`to`])):i(`v-if`,!0)],64))}})})))()}var Ie;function Le(){return(Le=e((()=>{z(),B(),Ce(),Fe(),x(),Ie=f({__name:`ToastClose`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`button`}},setup(e){let t=e,n=Me(),{forwardRef:r}=R();return(e,i)=>(u(),h(Se,{"as-child":``},{default:T(()=>[a(g(V),d(t,{ref:g(r),type:e.as===`button`?`button`:void 0,onClick:g(n).onClose}),{default:T(()=>[l(e.$slots,`default`)]),_:3},16,[`type`,`onClick`])]),_:3}))}})})))()}var Re;function ze(){return(ze=e((()=>{z(),Ce(),Le(),x(),Re=f({__name:`ToastAction`,props:{altText:{type:String,required:!0},asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){if(!e.altText)throw Error("Missing prop `altText` expected on `ToastAction`");let{forwardRef:t}=R();return(e,n)=>e.altText?(u(),h(Se,{key:0,"alt-text":e.altText,"as-child":``},{default:T(()=>[a(Ie,{ref:g(t),as:e.as,"as-child":e.asChild},{default:T(()=>[l(e.$slots,`default`)]),_:3},8,[`as`,`as-child`])]),_:3},8,[`alt-text`])):i(`v-if`,!0)}})})))()}var Be;function Ve(){return(Ve=e((()=>{z(),B(),x(),Be=f({__name:`ToastDescription`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){let t=e;return R(),(e,r)=>(u(),h(g(V),c(n(t)),{default:T(()=>[l(e.$slots,`default`)]),_:3},16))}})})))()}var He;function Ue(){return(Ue=e((()=>{de(),x(),He=f({__name:`ToastPortal`,props:{to:{type:null,required:!1},disabled:{type:Boolean,required:!1},defer:{type:Boolean,required:!1},forceMount:{type:Boolean,required:!1}},setup(e){let t=e;return(e,r)=>(u(),h(g(fe),c(n(t)),{default:T(()=>[l(e.$slots,`default`)]),_:3},16))}})})))()}var We;function Ge(){return(Ge=e((()=>{z(),se(),Fe(),x(),L(),We=f({__name:`ToastRoot`,props:{defaultOpen:{type:Boolean,required:!1,default:!0},forceMount:{type:Boolean,required:!1},type:{type:String,required:!1,default:`foreground`},open:{type:Boolean,required:!1,default:void 0},duration:{type:Number,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`li`}},emits:[`escapeKeyDown`,`pause`,`resume`,`swipeStart`,`swipeMove`,`swipeCancel`,`swipeEnd`,`update:open`],setup(e,{emit:t}){let n=e,r=t,{forwardRef:i}=R(),o=F(n,`open`,r,{defaultValue:n.defaultOpen,passive:n.open===void 0});return(e,t)=>(u(),h(g(ce),{present:e.forceMount||g(o)},{default:T(()=>[a(Pe,d({ref:g(i),open:g(o),type:e.type,as:e.as,"as-child":e.asChild,duration:e.duration},e.$attrs,{onClose:t[0]||=e=>o.value=!1,onPause:t[1]||=e=>r(`pause`),onResume:t[2]||=e=>r(`resume`),onEscapeKeyDown:t[3]||=e=>r(`escapeKeyDown`,e),onSwipeStart:t[4]||=e=>{r(`swipeStart`,e),e.defaultPrevented||e.currentTarget.setAttribute(`data-swipe`,`start`)},onSwipeMove:t[5]||=e=>{if(r(`swipeMove`,e),!e.defaultPrevented){let{x:t,y:n}=e.detail.delta,r=e.currentTarget;r.setAttribute(`data-swipe`,`move`),r.style.setProperty(`--reka-toast-swipe-move-x`,`${t}px`),r.style.setProperty(`--reka-toast-swipe-move-y`,`${n}px`)}},onSwipeCancel:t[6]||=e=>{if(r(`swipeCancel`,e),!e.defaultPrevented){let t=e.currentTarget;t.setAttribute(`data-swipe`,`cancel`),t.style.removeProperty(`--reka-toast-swipe-move-x`),t.style.removeProperty(`--reka-toast-swipe-move-y`),t.style.removeProperty(`--reka-toast-swipe-end-x`),t.style.removeProperty(`--reka-toast-swipe-end-y`)}},onSwipeEnd:t[7]||=e=>{if(r(`swipeEnd`,e),!e.defaultPrevented){let{x:t,y:n}=e.detail.delta,r=e.currentTarget;r.setAttribute(`data-swipe`,`end`),r.style.removeProperty(`--reka-toast-swipe-move-x`),r.style.removeProperty(`--reka-toast-swipe-move-y`),r.style.setProperty(`--reka-toast-swipe-end-x`,`${t}px`),r.style.setProperty(`--reka-toast-swipe-end-y`,`${n}px`),o.value=!1}}}),{default:T(({remaining:t,duration:n})=>[l(e.$slots,`default`,{remaining:t,duration:n,open:g(o)})]),_:3},16,[`open`,`type`,`as`,`as-child`,`duration`])]),_:3},8,[`present`]))}})})))()}var Ke;function qe(){return(qe=e((()=>{z(),B(),x(),Ke=f({__name:`ToastTitle`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1}},setup(e){let t=e;return R(),(e,r)=>(u(),h(g(V),c(n(t)),{default:T(()=>[l(e.$slots,`default`)]),_:3},16))}})})))()}var Je;function Ye(){return(Ye=e((()=>{_e(),G(),x(),Je=f({__name:`FocusProxy`,emits:[`focusFromOutsideViewport`],setup(e,{emit:t}){let n=t,r=W();return(e,t)=>(u(),h(g(ve),{tabindex:`0`,style:{position:`fixed`},onFocus:t[0]||=e=>{let t=e.relatedTarget;g(r).viewport.value?.contains(t)||n(`focusFromOutsideViewport`)}},{default:T(()=>[l(e.$slots,`default`)]),_:3}))}})})))()}var Xe;function Ze(){return(Ze=e((()=>{z(),B(),xe(),me(),H(),G(),je(),Ye(),x(),L(),Xe=f({inheritAttrs:!1,__name:`ToastViewport`,props:{hotkey:{type:Array,required:!1,default:()=>[`F8`]},label:{type:[String,Function],required:!1,default:`Notifications ({hotkey})`},asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`ol`}},setup(e){let{hotkey:t,label:n}=O(e),{forwardRef:r,currentElement:s}=R(),{CollectionSlot:c,getItems:f}=ge(),p=W(),m=b(()=>p.toastCount.value>0),_=w(),v=w(),y=/Key/g,x=/Digit/g,S=b(()=>t.value.join(`+`).replace(y,``).replace(x,``));re(t.value,()=>{s.value.focus()}),k(()=>{p.onViewportChange(s.value)}),ee(e=>{let t=s.value;if(m.value&&t){let n=()=>{if(!p.isClosePausedRef.value){let e=new CustomEvent(q);t.dispatchEvent(e),p.isClosePausedRef.value=!0}},r=()=>{if(p.isClosePausedRef.value){let e=new CustomEvent(J);t.dispatchEvent(e),p.isClosePausedRef.value=!1}},i=e=>{t.contains(e.relatedTarget)||r()},a=()=>{t.contains(oe())||r()},o=e=>{let n=e.altKey||e.ctrlKey||e.metaKey;if(e.key===`Tab`&&!n){let n=oe(),r=e.shiftKey;if(e.target===t&&r){_.value?.focus();return}let i=C({tabbingDirection:r?`backwards`:`forwards`}),a=i.findIndex(e=>e===n);pe(i.slice(a+1))?e.preventDefault():r?_.value?.focus():v.value?.focus()}};t.addEventListener(`focusin`,n),t.addEventListener(`focusout`,i),t.addEventListener(`pointermove`,n),t.addEventListener(`pointerleave`,a),t.addEventListener(`keydown`,o),window.addEventListener(`blur`,n),window.addEventListener(`focus`,r),e(()=>{t.removeEventListener(`focusin`,n),t.removeEventListener(`focusout`,i),t.removeEventListener(`pointermove`,n),t.removeEventListener(`pointerleave`,a),t.removeEventListener(`keydown`,o),window.removeEventListener(`blur`,n),window.removeEventListener(`focus`,r)})}});function C({tabbingDirection:e}){let t=f().map(e=>e.ref).map(t=>{let n=[t,...he(t)];return e===`forwards`?n:n.reverse()});return(e===`forwards`?t.reverse():t).flat()}return(e,t)=>(u(),h(g(be),{role:`region`,"aria-label":typeof g(n)==`string`?g(n).replace(`{hotkey}`,S.value):g(n)(S.value),tabindex:`-1`,style:o({pointerEvents:m.value?void 0:`none`})},{default:T(()=>[m.value?(u(),h(Je,{key:0,ref:e=>{e&&(_.value=g(ae)(e))},onFocusFromOutsideViewport:t[0]||=()=>{let e=C({tabbingDirection:`forwards`});g(pe)(e)}},null,512)):i(`v-if`,!0),a(g(c),null,{default:T(()=>[a(g(V),d({ref:g(r),tabindex:`-1`,as:e.as,"as-child":e.asChild},e.$attrs),{default:T(()=>[l(e.$slots,`default`)]),_:3},16,[`as`,`as-child`])]),_:3}),m.value?(u(),h(Je,{key:1,ref:e=>{e&&(v.value=g(ae)(e))},onFocusFromOutsideViewport:t[1]||=()=>{let e=C({tabbingDirection:`backwards`});g(pe)(e)}},null,512)):i(`v-if`,!0)]),_:3},8,[`aria-label`,`style`]))}})})))()}var Qe,$e,et,tt,nt,rt;function it(){return(it=e((()=>{x(),ze(),Le(),Ve(),Ge(),qe(),ye(),A(),Qe={class:`csp-toast__layout`},$e={key:0,class:`csp-toast__icon`},et={class:`csp-toast__content`},tt={key:2,class:`csp-toast__body`},nt={key:1,class:`csp-toast__actions`},rt=f({inheritAttrs:!1,__name:`CspToast`,props:{open:{type:Boolean,default:void 0},defaultOpen:{type:Boolean,default:!1},title:{default:null},description:{default:null},duration:{default:void 0},variant:{default:`default`},showIcon:{type:Boolean,default:!0},actionLabel:{default:null},actionAltText:{default:`Exécuter l'action`},showClose:{type:Boolean,default:!0},closeLabel:{default:`Fermer la notification`}},emits:[`update:open`,`action`],setup(e,{emit:t}){let n=e,r=t,o=v(),c=m(),f=b(()=>!!c.title||!!n.title),_=b(()=>!!c.description||!!n.description),y=b(()=>!!c.action||!!n.actionLabel),x={default:`ri:notification-3-line`,info:`ri:information-line`,success:`ri:checkbox-circle-line`,warning:`ri:alert-line`,error:`ri:error-warning-line`},ee=b(()=>x[n.variant]);return(t,n)=>(u(),h(g(We),d(g(o),{open:e.open,"default-open":e.defaultOpen,duration:e.duration,class:[`csp-toast`,`csp-toast--${e.variant}`],"onUpdate:open":n[1]||=e=>r(`update:open`,e)}),{default:T(()=>[D(`div`,Qe,[e.showIcon?(u(),E(`div`,$e,[l(t.$slots,`icon`,{},()=>[a(j,{name:ee.value},null,8,[`name`])])])):i(``,!0),D(`div`,et,[f.value?(u(),h(g(Ke),{key:0,as:`h3`,class:`csp-toast__title`},{default:T(()=>[l(t.$slots,`title`,{},()=>[s(p(e.title),1)])]),_:3})):i(``,!0),_.value?(u(),h(g(Be),{key:1,as:`p`,class:`csp-toast__description`},{default:T(()=>[l(t.$slots,`description`,{},()=>[s(p(e.description),1)])]),_:3})):i(``,!0),t.$slots.default?(u(),E(`div`,tt,[l(t.$slots,`default`)])):i(``,!0)]),y.value||e.showClose?(u(),E(`div`,nt,[y.value?(u(),h(g(Re),{key:0,"as-child":``,"alt-text":e.actionAltText,onClick:n[0]||=e=>r(`action`)},{default:T(()=>[l(t.$slots,`action`,{},()=>[a(U,{variant:`tertiary-no-outline`,size:`sm`,label:e.actionLabel},null,8,[`label`])])]),_:3},8,[`alt-text`])):i(``,!0),e.showClose?(u(),h(g(Ie),{key:1,"as-child":``},{default:T(()=>[a(U,{variant:`tertiary-no-outline`,size:`sm`,icon:`ri:close-line`,"aria-label":e.closeLabel},null,8,[`aria-label`])]),_:1})):i(``,!0)])):i(``,!0)])]),_:3},16,[`open`,`default-open`,`duration`,`class`]))}})})))()}var Y;function at(){return(at=e((()=>{it(),Y=rt})))()}var ot;function st(){return(st=e((()=>{x(),Ue(),G(),Ze(),ot=f({__name:`CspToastProvider`,props:{label:{default:`Notification`},duration:{default:3200},swipeDirection:{default:`right`},disableSwipe:{type:Boolean,default:!1}},setup(e){return(t,n)=>(u(),h(g(Te),{label:e.label,duration:e.duration,"disable-swipe":e.disableSwipe,"swipe-direction":e.swipeDirection},{default:T(()=>[l(t.$slots,`default`),a(g(He),null,{default:T(()=>[a(g(Xe),{class:`csp-toast-viewport`})]),_:1})]),_:3},8,[`label`,`duration`,`disable-swipe`,`swipe-direction`]))}})})))()}var X;function ct(){return(ct=e((()=>{st(),X=ot})))()}var lt,Z,Q,$,ut;function dt(){return(dt=e((()=>{x(),ye(),at(),ct(),lt={title:`Éléments/Génériques/CspToast`,component:Y,tags:[`autodocs`],parameters:{controls:{include:[`open`,`defaultOpen`,`title`,`description`,`duration`,`variant`,`showIcon`,`actionLabel`,`actionAltText`,`showClose`,`closeLabel`]},docs:{description:{component:`Notification toast accessible basée sur reka-ui. Doit être utilisé à l'intérieur d'un unique CspToastProvider placé à la racine de l'app.`}}},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},defaultOpen:{control:{type:`boolean`},description:`État d'ouverture initial en mode non contrôlé.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},title:{control:{type:`text`},description:"Titre du toast (ou slot `title`).",table:{type:{summary:`string | null`}}},description:{control:{type:`text`},description:"Description du toast (ou slot `description`).",table:{type:{summary:`string | null`}}},duration:{control:{type:`number`},description:`Durée d'affichage en millisecondes. Hérite du provider si non défini.`,table:{type:{summary:`number`}}},variant:{control:{type:`radio`},options:[`default`,`info`,`success`,`warning`,`error`],description:`Variante visuelle de la notification.`,table:{type:{summary:`default | info | success | warning | error`},defaultValue:{summary:`default`}}},showIcon:{control:{type:`boolean`},description:`Affiche ou masque l'icone.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},actionLabel:{control:{type:`text`},description:`Label du bouton d'action.`,table:{type:{summary:`string | null`}}},actionAltText:{control:{type:`text`},description:`Texte alternatif annoncé pour l'action.`,table:{type:{summary:`string`},defaultValue:{summary:`Exécuter l'action`}}},showClose:{control:{type:`boolean`},description:`Affiche ou masque le bouton de fermeture.`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}},closeLabel:{control:{type:`text`},description:`Libellé accessible du bouton de fermeture.`,table:{type:{summary:`string`},defaultValue:{summary:`Fermer la notification`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{defaultOpen:!1,title:`Action terminée`,description:`Votre modification a bien été enregistrée.`,variant:`success`,showIcon:!0,actionLabel:`Annuler`,actionAltText:`Annuler la dernière action`,showClose:!0,closeLabel:`Fermer la notification`},render:e=>({components:{CspButton:U,CspToast:Y,CspToastProvider:X},setup(){let n=w(!!e.open);t(()=>e.open,e=>{e!==void 0&&(n.value=e)});function r(){n.value=!0}function i(e){n.value=e}return{args:e,open:n,showToast:r,handleUpdateOpen:i}},template:`
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
    `})},Z={},Q={render:e=>({components:{CspButton:U,CspToast:Y,CspToastProvider:X},setup(){let t=[`default`,`info`,`success`,`warning`,`error`],n=w(!1),r=w(`default`);function i(e){r.value=e,n.value=!0}function a(e){n.value=e}return{args:e,variants:t,open:n,currentVariant:r,openVariant:i,updateOpen:a}},template:`
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
    `})},$={render:()=>({components:{CspButton:U,CspToast:Y,CspToastProvider:X},setup(){let e=w([]),t=0;function n(n){e.value.push({id:t++,variant:n,title:`Notification ${n} #${t}`})}function r(t){e.value=e.value.filter(e=>e.id!==t)}return{toasts:e,addToast:n,removeToast:r}},template:`
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