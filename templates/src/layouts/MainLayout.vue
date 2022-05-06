<template>
  <div class="q-pa-md">
    <q-layout view="hHh Lpr lFf">
      <q-header>
        <q-toolbar>
          <q-btn
            flat
            dense
            round
            icon="pets"
            aria-label="Menu"
            @click="leftDrawerOpen = !leftDrawerOpen"
          />

          <q-toolbar-title>
            <q-btn
            flat
            aria-label="SKYLLA"
            @click="go_main"
          >Σ SKYLLA</q-btn>
          </q-toolbar-title>

          <div>Quasar v{{ $q.version }}</div>
        </q-toolbar>
      </q-header>

      <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
        <q-list v-for="m in menu" :key="m.categoria" padding dense>
          <q-item-label header class="text-subtitle1 text-grey-8 text-weight-light">
            <q-icon style="margin-top: -4px;" :name="m.icon" />
            {{ m.categoria }}
          </q-item-label>
          <q-item style="width: 100%">
            <div style="width:100%">
            <q-btn
              no-caps
              align="left"
              class="full-width text-grey-8 text-weight-light"
              flat
              v-for="item in m.items"
              :key="item.titulo"
              v-show="item.visivel"
              @click="$router.push(item.path).catch(err=>{})"
              :icon="item.icon"
              :label="item.titulo"
            >
            </q-btn>
            </div>
          </q-item>
        </q-list>
      </q-drawer>

      <q-page-container>
        <router-view />
      </q-page-container>
    </q-layout>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api';
import { SessionStorage } from 'quasar';

export default defineComponent({
  name: 'MainLayout',
  components: {},
  setup() {
    const leftDrawerOpen = ref(false);
    return { leftDrawerOpen };
  },
  data() {
    return {
      menu: [
        {
          categoria: 'Busca',
          visivel: true,
          icon: 'search',
          items: [
            {
              titulo: 'Cliente',
              visivel: true,
              icon: 'person',
              path: '/cliente/busca'
            },
            {
              titulo: 'Animal',
              visivel: true,
              icon: 'pets',
              path: '/animal/busca'
            },
            {
              titulo: 'Medicamento',
              visivel: true,
              icon: 'medication',
              path: '/medicamento/busca'
            },
            {
              titulo: 'Doença',
              visivel: true,
              icon: 'coronavirus',
              path: '/doenca/busca'
            },
            {
              titulo: 'Receituário',
              visivel: true,
              icon: 'description',
              path: '/receituario/busca'
            },
            {
              titulo: 'Atendimento',
              visivel: true,
              icon: 'event_note',
              path: '/atendimento/busca'
            },
            {
              titulo: 'Consulta',
              visivel: true,
              icon: 'event_note',
              path: '/consulta/busca'
            },
            {
              titulo: 'Cirurgia',
              visivel: true,
              icon: 'event_note',
              path: '/cirurgia/busca'
            },
            {
              titulo: 'Emergência',
              visivel: true,
              icon: 'event_note',
              path: '/emergencia/busca'
            },
          ]
        },
        {
          categoria: 'Cadastro',
          visivel: true,
          icon: 'add',
          items: [
            {
              titulo: 'Cliente',
              visivel: true,
              icon: 'person',
              path: '/cliente/cadastro'
            },
            {
              titulo: 'Animal',
              visivel: true,
              icon: 'pets',
              path: '/animal/cadastro'
            },
            {
              titulo: 'Medicamento',
              visivel: true,
              icon: 'medication',
              path: '/medicamento/cadastro'
            },
            {
              titulo: 'Doença',
              visivel: true,
              icon: 'coronavirus',
              path: '/doenca/cadastro'
            },
            {
              titulo: 'Receituário',
              visivel: true,
              icon: 'description',
              path: '/receituario/cadastro'
            },
          ]
        },
        {
          categoria: 'Relatórios',
          visivel: true,
          icon: 'content_paste',
          items: [
            {
              titulo: 'Relatório de Clientes',
              visivel: true,
              icon: 'content_paste',
              path: '/relatorios/cliente'
            },
          ]
        }
      ]
    };
  },
  methods: {
    checar_token: function() {
      if (SessionStorage.getItem('token') == null) {
        this.$router.push('/login');
      }
    },
    go_main:function(){
      this.$router.push('/');
    }
  },
  mounted: function() {
    this.checar_token();
  }
});
</script>
