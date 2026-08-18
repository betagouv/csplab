import{n as e}from"./rolldown-runtime-DkW27tQK.js";import{Ct as t,D as n,E as r,F as i,K as a,P as o,R as s,S as c,V as l,W as u,X as d,Z as ee,c as f,ft as p,gt as te,k as m,m as h,tt as g,x as _,yt as v}from"./iframe-CrUhtth-.js";import{E as ne,T as re,d as ie,g as ae,i as oe,n as y,t as b,y as se}from"./useForwardExpose-BdmqqYSy.js";import{n as ce,t as x}from"./Primitive-Ba3BVjgw.js";import{n as S,t as C}from"./useId-sfLorONq.js";import{a as le,i as ue,n as de,o as fe,r as pe,t as me}from"./FocusScope-DwcW0j6J.js";import{n as he,t as ge}from"./useFocusGuards-ByJUPNbi.js";import{a as _e,c as ve,d as ye,f as be,l as w,n as xe,o as Se,r as Ce,s as we,u as T}from"./PopperContent-DfUyEwsi.js";import{n as Te,t as Ee}from"./Presence-CjA7cFCI.js";import{a as De,n as E,r as Oe,t as ke}from"./Teleport-D8_wKn2h.js";import{n as Ae,t as D}from"./CspButton-DWH4jZfL.js";import{n as je,t as Me}from"./useStoryOpenState-B0DdPASZ.js";var O,k,A;function j(){return(j=e((()=>{ne(),ve(),f(),oe(),[O,k]=re(`PopoverRoot`),A=n({__name:`PopoverRoot`,props:{defaultOpen:{type:Boolean,required:!1,default:!1},open:{type:Boolean,required:!1,default:void 0},modal:{type:Boolean,required:!1,default:!1}},emits:[`update:open`],setup(e,{emit:t}){let n=e,r=t,{modal:i}=te(n),a=ie(n,`open`,r,{defaultValue:n.defaultOpen,passive:n.open===void 0}),o=p(),s=p(!1);return k({contentId:``,triggerId:``,modal:i,open:a,onOpenChange:e=>{a.value=e},onOpenToggle:()=>{a.value=!a.value},triggerElement:o,hasCustomAnchor:s}),(e,t)=>(l(),_(v(we),null,{default:g(()=>[u(e.$slots,`default`,{open:v(a),close:()=>a.value=!1})]),_:3}))}})})))()}var M;function N(){return(N=e((()=>{ge(),b(),ye(),De(),de(),Ce(),j(),f(),ae(),M=n({__name:`PopoverContentImpl`,props:{trapFocus:{type:Boolean,required:!1},side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let n=e,a=t,o=be(se(n,`trapFocus`,`disableOutsidePointerEvents`)),{forwardRef:s}=y(),c=O();return he(),(e,t)=>(l(),_(v(me),{"as-child":``,loop:``,trapped:e.trapFocus,onMountAutoFocus:t[5]||=e=>a(`openAutoFocus`,e),onUnmountAutoFocus:t[6]||=e=>a(`closeAutoFocus`,e)},{default:g(()=>[r(v(Oe),{"as-child":``,"disable-outside-pointer-events":e.disableOutsidePointerEvents,onPointerDownOutside:t[0]||=e=>a(`pointerDownOutside`,e),onInteractOutside:t[1]||=e=>a(`interactOutside`,e),onEscapeKeyDown:t[2]||=e=>a(`escapeKeyDown`,e),onFocusOutside:t[3]||=e=>a(`focusOutside`,e),onDismiss:t[4]||=e=>v(c).onOpenChange(!1)},{default:g(()=>[r(v(xe),i(v(o),{id:v(c).contentId,ref:v(s),"data-state":v(c).open.value?`open`:`closed`,"aria-labelledby":v(c).triggerId,style:{"--reka-popover-content-transform-origin":`var(--reka-popper-transform-origin)`,"--reka-popover-content-available-width":`var(--reka-popper-available-width)`,"--reka-popover-content-available-height":`var(--reka-popper-available-height)`,"--reka-popover-trigger-width":`var(--reka-popper-anchor-width)`,"--reka-popover-trigger-height":`var(--reka-popper-anchor-height)`},role:`dialog`}),{default:g(()=>[u(e.$slots,`default`)]),_:3},16,[`id`,`data-state`,`aria-labelledby`])]),_:3},8,[`disable-outside-pointer-events`])]),_:3},8,[`trapped`]))}})})))()}var P;function F(){return(F=e((()=>{le(),b(),w(),pe(),j(),N(),f(),P=n({__name:`PopoverContentModal`,props:{side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let n=e,r=t,a=O(),o=p(!1);fe(!0);let s=T(n,r),{forwardRef:c,currentElement:d}=y();return ue(d),(e,t)=>(l(),_(M,i(v(s),{ref:v(c),"trap-focus":v(a).open.value,"disable-outside-pointer-events":``,onCloseAutoFocus:t[0]||=h(e=>{r(`closeAutoFocus`,e),o.value||v(a).triggerElement.value?.focus()},[`prevent`]),onPointerDownOutside:t[1]||=e=>{r(`pointerDownOutside`,e);let t=e.detail.originalEvent,n=t.button===0&&t.ctrlKey===!0,i=t.button===2||n;o.value=i},onFocusOutside:t[2]||=h(()=>{},[`prevent`])}),{default:g(()=>[u(e.$slots,`default`)]),_:3},16,[`trap-focus`]))}})})))()}var I;function L(){return(L=e((()=>{w(),j(),N(),f(),I=n({__name:`PopoverContentNonModal`,props:{side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let n=e,r=t,a=O(),o=p(!1),s=p(!1),c=T(n,r);return(e,t)=>(l(),_(M,i(v(c),{"trap-focus":!1,"disable-outside-pointer-events":!1,onCloseAutoFocus:t[0]||=e=>{r(`closeAutoFocus`,e),e.defaultPrevented||(o.value||v(a).triggerElement.value?.focus(),e.preventDefault()),o.value=!1,s.value=!1},onInteractOutside:t[1]||=async e=>{r(`interactOutside`,e),e.defaultPrevented||(o.value=!0,e.detail.originalEvent.type===`pointerdown`&&(s.value=!0));let t=e.target;v(a).triggerElement.value?.contains(t)&&e.preventDefault(),e.detail.originalEvent.type===`focusin`&&s.value&&e.preventDefault()}}),{default:g(()=>[u(e.$slots,`default`)]),_:3},16))}})})))()}var R;function z(){return(z=e((()=>{b(),w(),C(),Te(),j(),F(),L(),f(),R=n({__name:`PopoverContent`,props:{forceMount:{type:Boolean,required:!1},side:{type:null,required:!1},sideOffset:{type:Number,required:!1},sideFlip:{type:Boolean,required:!1},align:{type:null,required:!1},alignOffset:{type:Number,required:!1},alignFlip:{type:Boolean,required:!1},avoidCollisions:{type:Boolean,required:!1},collisionBoundary:{type:null,required:!1},collisionPadding:{type:[Number,Object],required:!1},arrowPadding:{type:Number,required:!1},hideShiftedArrow:{type:Boolean,required:!1},sticky:{type:String,required:!1},hideWhenDetached:{type:Boolean,required:!1},positionStrategy:{type:String,required:!1},updatePositionStrategy:{type:String,required:!1},disableUpdateOnLayoutShift:{type:Boolean,required:!1},prioritizePosition:{type:Boolean,required:!1},reference:{type:null,required:!1},asChild:{type:Boolean,required:!1},as:{type:null,required:!1},disableOutsidePointerEvents:{type:Boolean,required:!1}},emits:[`escapeKeyDown`,`pointerDownOutside`,`focusOutside`,`interactOutside`,`openAutoFocus`,`closeAutoFocus`],setup(e,{emit:t}){let n=e,r=t,a=O(),o=T(n,r),{forwardRef:s}=y();return a.contentId||=S(void 0,`reka-popover-content`),(e,t)=>(l(),_(v(Ee),{present:e.forceMount||v(a).open.value},{default:g(()=>[v(a).modal.value?(l(),_(P,i({key:0},v(o),{ref:v(s)}),{default:g(()=>[u(e.$slots,`default`)]),_:3},16)):(l(),_(I,i({key:1},v(o),{ref:v(s)}),{default:g(()=>[u(e.$slots,`default`)]),_:3},16))]),_:3},8,[`present`]))}})})))()}var B;function V(){return(V=e((()=>{E(),f(),B=n({__name:`PopoverPortal`,props:{to:{type:null,required:!1},disabled:{type:Boolean,required:!1},defer:{type:Boolean,required:!1},forceMount:{type:Boolean,required:!1}},setup(e){let n=e;return(e,r)=>(l(),_(v(ke),t(m(n)),{default:g(()=>[u(e.$slots,`default`)]),_:3},16))}})})))()}var H;function U(){return(U=e((()=>{b(),C(),ce(),Se(),j(),f(),H=n({__name:`PopoverTrigger`,props:{asChild:{type:Boolean,required:!1},as:{type:null,required:!1,default:`button`}},setup(e){let t=e,n=O(),{forwardRef:i,currentElement:o}=y();return n.triggerId||=S(void 0,`reka-popover-trigger`),s(()=>{n.triggerElement.value=o.value}),(e,o)=>(l(),_(a(v(n).hasCustomAnchor.value?v(x):v(_e)),{"as-child":``},{default:g(()=>[r(v(x),{id:v(n).triggerId,ref:v(i),type:e.as===`button`?`button`:void 0,"aria-haspopup":`dialog`,"aria-expanded":v(n).open.value,"aria-controls":v(n).contentId,"data-state":v(n).open.value?`open`:`closed`,as:e.as,"as-child":t.asChild,onClick:v(n).onOpenToggle},{default:g(()=>[u(e.$slots,`default`)]),_:3},8,[`id`,`type`,`aria-expanded`,`aria-controls`,`data-state`,`as`,`as-child`,`onClick`])]),_:3}))}})})))()}var W;function G(){return(G=e((()=>{f(),z(),V(),j(),U(),W=n({inheritAttrs:!1,__name:`CspPopover`,props:o({side:{default:`bottom`},align:{default:`start`}},{open:{type:Boolean},openModifiers:{}}),emits:[`update:open`],setup(e){let t=d(e,`open`),n=!!ee().trigger;return(i,a)=>(l(),_(v(A),{open:t.value,"onUpdate:open":a[0]||=e=>t.value=e},{default:g(()=>[v(n)?(l(),_(v(H),{key:0,"as-child":``},{default:g(()=>[u(i.$slots,`trigger`)]),_:3})):c(``,!0),r(v(B),null,{default:g(()=>[r(v(R),{class:`csp-popover`,side:e.side,align:e.align,"side-offset":6},{default:g(()=>[u(i.$slots,`default`)]),_:3},8,[`side`,`align`])]),_:3})]),_:3},8,[`open`]))}})})))()}var K;function q(){return(q=e((()=>{G(),K=W})))()}var J,Y,X,Z,Q;function $(){return($=e((()=>{Ae(),q(),Me(),J={title:`Éléments/Génériques/CspPopover`,component:K,tags:[`autodocs`],parameters:{controls:{include:[`open`,`side`,`align`]},docs:{description:{component:"Popover générique construit sur la primitive `reka-ui`. Affiche un contenu flottant ancré à un déclencheur via le slot `trigger`. Gère le focus, la touche Échap et le clic extérieur. Le slot par défaut reçoit le contenu libre."}},layout:`centered`},argTypes:{open:{control:{type:`boolean`},description:"État d'ouverture contrôlé. Liez avec `v-model:open`.",table:{type:{summary:`boolean`}}},side:{control:{type:`radio`},options:[`top`,`right`,`bottom`,`left`],description:`Côté d'apparition du popover.`,table:{type:{summary:`top | right | bottom | left`},defaultValue:{summary:`bottom`}}},align:{control:{type:`radio`},options:[`start`,`center`,`end`],description:`Alignement du popover par rapport au déclencheur.`,table:{type:{summary:`start | center | end`},defaultValue:{summary:`start`}}},trigger:{control:!1,table:{disable:!0}},default:{control:!1,table:{disable:!0}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}},args:{side:`bottom`,align:`start`},render:e=>({components:{CspPopover:K,CspButton:D},setup(){let{controlledOpen:t,handleUpdateOpen:n,open:r}=je(e);return{args:e,controlledOpen:t,handleUpdateOpen:n,open:r}},template:`
      <CspPopover v-bind="args" :open="controlledOpen" @update:open="handleUpdateOpen">
        <template #trigger>
          <CspButton
            :label="(open ? 'Fermer' : 'Ouvrir') + ' le popover'"
            variant="secondary"
            icon="ri:settings-3-line"
            :is-icon-left="true"
          />
        </template>

        <p class="text-sm">Contenu libre du popover.</p>
      </CspPopover>
    `})},Y={name:`Par défaut`},X={name:`Côtés`,render:e=>({components:{CspPopover:K,CspButton:D},setup(){return{args:e,sides:[{label:`Haut`,value:`top`},{label:`Droite`,value:`right`},{label:`Bas`,value:`bottom`},{label:`Gauche`,value:`left`}]}},template:`
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 justify-items-center">
        <div v-for="s in sides" :key="s.value" class="p-8">
          <CspPopover
            v-bind="args"
            :side="s.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover côté ' + s.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>

            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    `})},Z={name:`Alignements`,render:e=>({components:{CspPopover:K,CspButton:D},setup(){return{args:e,alignments:[{label:`Début`,value:`start`},{label:`Centre`,value:`center`},{label:`Fin`,value:`end`}]}},template:`
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 justify-items-center">
        <div v-for="a in alignments" :key="a.value" class="p-8">
          <CspPopover
            v-bind="args"
            :align="a.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover aligné ' + a.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>
            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    `})},Y.parameters={...Y.parameters,docs:{...Y.parameters?.docs,source:{originalSource:`{
  name: 'Par défaut'
}`,...Y.parameters?.docs?.source}}},X.parameters={...X.parameters,docs:{...X.parameters?.docs,source:{originalSource:`{
  name: 'Côtés',
  render: (args: CspPopoverProps) => ({
    components: {
      CspPopover,
      CspButton
    },
    setup() {
      const sides = [{
        label: 'Haut',
        value: 'top'
      }, {
        label: 'Droite',
        value: 'right'
      }, {
        label: 'Bas',
        value: 'bottom'
      }, {
        label: 'Gauche',
        value: 'left'
      }] satisfies {
        label: string;
        value: NonNullable<CspPopoverProps['side']>;
      }[];
      return {
        args,
        sides
      };
    },
    template: \`
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 justify-items-center">
        <div v-for="s in sides" :key="s.value" class="p-8">
          <CspPopover
            v-bind="args"
            :side="s.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover côté ' + s.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>

            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    \`
  })
}`,...X.parameters?.docs?.source}}},Z.parameters={...Z.parameters,docs:{...Z.parameters?.docs,source:{originalSource:`{
  name: 'Alignements',
  render: (args: CspPopoverProps) => ({
    components: {
      CspPopover,
      CspButton
    },
    setup() {
      const alignments = [{
        label: 'Début',
        value: 'start'
      }, {
        label: 'Centre',
        value: 'center'
      }, {
        label: 'Fin',
        value: 'end'
      }] satisfies {
        label: string;
        value: NonNullable<CspPopoverProps['align']>;
      }[];
      return {
        args,
        alignments
      };
    },
    template: \`
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 justify-items-center">
        <div v-for="a in alignments" :key="a.value" class="p-8">
          <CspPopover
            v-bind="args"
            :align="a.value"
          >
            <template #trigger>
              <CspButton
                :label="(controlledOpen ? 'Fermer' : 'Ouvrir') + ' le popover aligné ' + a.label.toLowerCase()"
                variant="secondary"
                icon="ri:settings-3-line"
                :is-icon-left="true"
              />
            </template>
            <p class="text-sm">Contenu libre du popover</p>
          </CspPopover>
        </div>
      </div>
    \`
  })
}`,...Z.parameters?.docs?.source}}},Q=[`Default`,`Sides`,`Alignments`]})))()}$();export{Z as Alignments,Y as Default,X as Sides,Q as __namedExportsOrder,J as default};