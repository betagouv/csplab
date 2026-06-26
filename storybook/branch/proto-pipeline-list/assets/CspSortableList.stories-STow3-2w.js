import{i as e}from"./preload-helper-QkcEG8nj.js";import{D as t,jt as n}from"./iframe-ByzLeagf.js";import{n as r,t as i}from"./CspButton-8u3AJ3l5.js";import{n as a,t as o}from"./CspDropdownMenu-CeEKu20o.js";import{n as s,t as c}from"./CspSortableList-C3tsx88O.js";var l,u,d,f,p;e((()=>{t(),r(),a(),s(),l={title:`Éléments/Génériques/CspSortableList`,component:c,tags:[`autodocs`],parameters:{docs:{description:{component:"Liste réordonnable par drag and drop. Accessible via les fonctions `moveUp`/`moveDown` exposées dans le slot."}}},argTypes:{items:{control:!1,description:`Liste des éléments à afficher.`,table:{type:{summary:`T[]`}}},getItemKey:{control:!1,description:`Fonction retournant la clé unique de chaque élément.`,table:{type:{summary:`(item: T) => string`}}},getItemLabel:{control:!1,description:`Fonction retournant le libellé pour les annonces d'accessibilité.`,table:{type:{summary:`(item: T) => string`}}},isItemDraggable:{control:!1,description:`Fonction déterminant si un élément est déplaçable.`,table:{type:{summary:`(item: T, index: number) => boolean`},defaultValue:{summary:`() => true`}}},getItemVariant:{control:!1,description:`Fonction retournant la variante visuelle de chaque élément.`,table:{type:{summary:`(item: T, index: number) => 'default' | 'alt'`},defaultValue:{summary:`() => 'default'`}}},disabled:{control:{type:`boolean`},description:`Désactive le drag and drop sur toute la liste.`,table:{type:{summary:`boolean`},defaultValue:{summary:`false`}}},onReorder:{action:`reorder`,description:`Émis quand la liste est réordonnée.`,table:{category:`Events`,type:{summary:`(items: T[]) => void`}}},item:{control:!1,description:"Slot pour personnaliser le contenu de chaque élément. Expose : `item`, `index`, `isDragging`, `isDraggable`, `canMoveUp`, `canMoveDown`, `moveUp`, `moveDown`.",table:{category:`Slots`,type:{summary:`slot`}}},class:{control:!1,table:{disable:!0}},style:{control:!1,table:{disable:!0}},key:{control:!1,table:{disable:!0}},ref:{control:!1,table:{disable:!0}},ref_for:{control:!1,table:{disable:!0}},ref_key:{control:!1,table:{disable:!0}}}},u={render:()=>({components:{CspSortableList:c},setup(){let e=n([{id:`1`,label:`Élément 1`},{id:`2`,label:`Élément 2`},{id:`3`,label:`Élément 3`},{id:`4`,label:`Élément 4`}]);function t(t){e.value=t}return{items:e,getItemKey:e=>e.id,getItemLabel:e=>e.label,onReorder:t}},template:`
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
    `})},d={render:()=>({components:{CspSortableList:c},setup(){let e=n([{id:`1`,label:`Élément épinglé`,pinned:!0},{id:`2`,label:`Élément 2`},{id:`3`,label:`Élément 3`},{id:`4`,label:`Élément 4`},{id:`5`,label:`Élément 5`}]);function t(t){t.findIndex(e=>e.pinned)===0&&(e.value=t)}return{items:e,getItemKey:e=>e.id,getItemLabel:e=>e.label,isItemDraggable:e=>!e.pinned,getItemVariant:e=>e.pinned?`alt`:`default`,onReorder:t}},template:`
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
    `})},f={render:()=>({components:{CspSortableList:c,CspButton:i,CspDropdownMenu:o},setup(){let e=n([{id:`1`,label:`Élément 1`},{id:`2`,label:`Élément 2`},{id:`3`,label:`Élément 3`},{id:`4`,label:`Élément 4`}]);function t(t){e.value=t}function r(t){e.value=e.value.filter(e=>e.id!==t)}function i(e,t,n,i,a){return[{items:[{label:`Monter`,icon:`ri:arrow-up-s-line`,disabled:!e,onSelect:n},{label:`Descendre`,icon:`ri:arrow-down-s-line`,disabled:!t,onSelect:i}]},{items:[{label:`Supprimer`,icon:`ri:delete-bin-line`,destructive:!0,onSelect:()=>r(a)}]}]}return{items:e,getItemKey:e=>e.id,getItemLabel:e=>e.label,onReorder:t,getMenuSections:i}},template:`
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
    `})},u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
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
}`,...u.parameters?.docs?.source}}},d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
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
}`,...d.parameters?.docs?.source}}},f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
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
}`,...f.parameters?.docs?.source}}},p=[`Default`,`WithPinnedItems`,`WithActions`]}))();export{u as Default,f as WithActions,d as WithPinnedItems,p as __namedExportsOrder,l as default};