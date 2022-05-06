<template>
 <q-page class="row justify-center">
    <!-- <q-btn color="white" text-color="black" label="Trocar" @click="$router.push('/busca/123')" /> -->
  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api';

export default defineComponent({
  name: 'PageIndex',
  components: { },
  data(){
    return {
      busca: false,
    }
  }
});
</script>
