import{i as e}from"./preload-helper-CuYJbHmM.js";import{D as t,jt as n}from"./iframe-iJ1RGaZ4.js";import{n as r,t as i}from"./CspIcon-CZJFwYU3.js";import{n as a,t as o}from"./CspButton-B9zfljql.js";import{n as s,t as c}from"./CspSortableList-BGUx4QIE.js";var l,u,d,f,p,m,h,g;e((()=>{t(),a(),r(),s(),l={title:`Éléments/Génériques/CspSortableList`,component:c,tags:[`autodocs`],parameters:{controls:{include:[`showAccessibilityButtons`]}},argTypes:{showAccessibilityButtons:{control:{type:`boolean`},description:`Afficher les boutons monter/descendre (accessibilité).`,table:{type:{summary:`boolean`},defaultValue:{summary:`true`}}}},args:{showAccessibilityButtons:!0}},u={display:`flex`,alignItems:`center`,gap:`var(--csp-space-3)`,padding:`var(--csp-space-3) var(--csp-space-4)`,borderRadius:`0.25rem`,boxShadow:`inset 0 0 0 1px var(--border-default-grey)`,background:`var(--background-default-grey)`},d={display:`flex`,cursor:`grab`,color:`var(--text-mention-grey)`},f={display:`flex`,gap:`var(--csp-space-1)`,minWidth:`4rem`},p={render:e=>({components:{CspSortableList:c,CspIcon:i,CspButton:o},setup(){let t=n([{id:`1`,label:`Pré-qualification`},{id:`2`,label:`Entretien téléphonique`},{id:`3`,label:`Entretien technique`},{id:`4`,label:`Entretien RH`}]);function r(e){t.value=e}return{args:e,items:t,itemStyle:u,handleStyle:d,actionsStyle:f,getItemKey:e=>e.id,getItemLabel:e=>e.label,onReorder:r}},template:`
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
    `})},m={display:`flex`,color:`var(--text-mention-grey)`},h={args:{showAccessibilityButtons:!0},render:e=>({components:{CspSortableList:c,CspIcon:i,CspButton:o},setup(){let t=n([{id:`1`,label:`Candidature reçue`,locked:!0},{id:`2`,label:`Pré-qualification`},{id:`3`,label:`Entretien`},{id:`4`,label:`Entretien RH`},{id:`5`,label:`Offre clôturée`,locked:!0}]);function r(e){t.value=e}return{args:e,items:t,itemStyle:u,iconStyle:m,actionsStyle:f,getItemKey:e=>e.id,getItemLabel:e=>e.label,isItemDraggable:e=>!e.locked,onReorder:r}},template:`
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
    `})},p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
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
}`,...p.parameters?.docs?.source}}},h.parameters={...h.parameters,docs:{...h.parameters?.docs,source:{originalSource:`{
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
}`,...h.parameters?.docs?.source}}},g=[`Default`,`WithLockedItems`]}))();export{p as Default,h as WithLockedItems,g as __namedExportsOrder,l as default};