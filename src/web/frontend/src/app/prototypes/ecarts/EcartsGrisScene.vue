<script setup lang="ts">
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import CspSkeletonKanban from '@/components/base/CspSkeleton/CspSkeletonKanban.vue'
import CspSkeletonTable from '@/components/base/CspSkeleton/CspSkeletonTable.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
</script>

<template>
  <div class="ecarts-gris">
    <div class="ecarts-gris__row">
      <div class="ecarts-gris__lines">
        <CspSkeleton
          width="12rem"
          height="1.25rem"
        />
        <CspSkeleton width="16rem" />
        <CspSkeleton width="10rem" />
      </div>

      <div class="ecarts-gris__neutrals">
        <CspAvatar name="Camille Martin" />
        <CspBadge label="Brouillon" />
        <CspTag label="Archivé" />
      </div>
    </div>

    <CspSkeletonTable
      :rows="3"
      :columns="3"
    />

    <CspSkeletonKanban
      :columns="2"
      :cards="1"
    />
  </div>
</template>

<style scoped lang="scss">
.ecarts-gris {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
  padding: var(--csp-space-6);
}

.ecarts-gris__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-6);
}

.ecarts-gris__lines {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.ecarts-gris__neutrals {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
}
</style>
