<template>
  <q-page padding class="full-width">
    <q-form @submit="salvar">
      <div class="row">
        <div class="col">
          <q-btn
            label="Voltar"
            color="negative"
            flat
            icon="arrow_back"
            @click="voltar_busca"
          />
        </div>
      </div>
      <div class="row">
        <div class="col text-h5 text-weight-light">
          Registro de Medicamento Administrado
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-select
            outlined
            dense
            use-input
            v-model="form.consulta__id"
            :options="data"
            label="Consulta"
            option-label="id"
            option-value="id"
            emit-value
            map-options
            @filter="filtrar"
            :readonly="consulta_bool"
            v-show="consulta_bool"
          />
          <q-select
            outlined
            dense
            use-input
            v-model="form.cirurgia__id"
            :options="data"
            label="Cirurgia"
            option-label="id"
            option-value="id"
            emit-value
            map-options
            @filter="filtrar"
            :readonly="cirurgia_bool"
            v-show="cirurgia_bool"
          />
          <q-select
            outlined
            dense
            use-input
            v-model="form.emergencia__id"
            :options="data"
            label="Emergência"
            option-label="id"
            option-value="id"
            emit-value
            map-options
            @filter="filtrar"
            :readonly="emergencia_bool"
            v-show="emergencia_bool"
          />
          <q-select
            outlined
            dense
            use-input
            v-model="form.atendimento__id"
            :options="data"
            label="Atendimento"
            option-label="id"
            option-value="id"
            emit-value
            map-options
            @filter="filtrar"
            :readonly="atendimento_bool"
            v-show="atendimento_bool"
          />
        </div>
        <div class="col">
          <q-select
            outlined
            dense
            use-input
            v-model="form.medicamento__id"
            :options="data_medicamento"
            label="Medicamento"
            option-label="medicamento"
            option-value="id"
            emit-value
            map-options
            @filter="filtrar_medicamento"
          />
        </div>
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.quantidade_administrada"
            label="Quantidade Administrada"
          />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.data_aplicacao"
            label="Data da Aplicação"
            type="date"
          />
        </div>
        <div class="col">
          <q-input
            outlined
            dense
            v-model="form.observacao"
            label="Observação"
            type="textarea"
          />
        </div>
        <div class="col">
          <!-- ajustar campos -->
        </div>
      </div>
      <div class="column items-end">
        <div class="col">
          <q-btn label="Salvar" flat icon-right="done" type="submit" />
        </div>
      </div>
    </q-form>
  </q-page>
</template>

<script>
import { defineComponent } from '@vue/composition-api';
import {
  save,
  get
} from './../../services/veterinaria/MedicamentoAdministradoService';
import { findall as findall_medicamento } from './../../services/veterinaria/MedicamentoService'
import { findall as findall_consulta } from './../../services/veterinaria/ConsultaService'
import { findall as findall_cirurgia } from './../../services/veterinaria/CirurgiaService'
import { findall as findall_emergencia } from './../../services/veterinaria/EmergenciaService'
import { findall as findall_atendimento } from './../../services/veterinaria/AtendimentoService'

export default defineComponent({
  name: 'MedicamentoAdministradoCadastroView',
  data() {
    return {
      form: {
        
      },
      data: [],
      data_medicamento: [],
      filtro: undefined,
      filtro_medicamento: undefined,
      pk: undefined,
      consulta: undefined,
      cirurgia: undefined,
      emergencia: undefined,
      atendimento: undefined,
      consulta_bool: false,
      cirurgia_bool: false,
      emergencia_bool: false,
      atendimento_bool: false,
    };
  },
  methods: {
    voltar_busca: function() {
      if (this.consulta != null) {
        this.$router.push(`/medicamento_administrado/busca/consulta/${this.consulta}`);
      } else if (this.cirurgia != null) {
        this.$router.push(`/medicamento_administrado/busca/cirurgia/${this.cirurgia}`);
      } else if (this.emergencia != null) {
        this.$router.push(`/medicamento_administrado/busca/emergencia/${this.emergencia}`);
      } else if (this.atendimento != null) {
        this.$router.push(`/medicamento_administrado/busca/atendimento/${this.atendimento}`);
      }
    },
    salvar: function() {
      save(this);
    },
    filtrar: function(val, update, abort) {
      this.filtro = val;
      if (this.consulta != null) {
        findall_consulta(this)
      } else if (this.cirurgia != null) {
        findall_cirurgia(this)
      } else if (this.emergencia != null) {
        findall_emergencia(this)
      } else if (this.atendimento != null) {
        findall_atendimento(this)
      }
      update(() => {
        this.data = this.data;
      });
    },
    filtrar_medicamento: function(val, update, abort) {
      this.filtro_medicamento = val;
      findall_medicamento(this)
      update(() => {
        this.data_medicamento = this.data_medicamento;
      });
    },
    editar: function() {
      get(this);
    },
  },
  mounted: function() {
    if (this.$route.params.consulta != null) {
      this.consulta = this.$route.params.consulta;
      this.form.consulta__id = this.consulta;
      this.consulta_bool = true
    } else if (this.$route.params.cirurgia != null) {
      this.cirurgia = this.$route.params.cirurgia;
      this.form.cirurgia__id = this.cirurgia;
      this.cirurgia_bool = true
    } else if (this.$route.params.emergencia != null) {
      this.emergencia = this.$route.params.emergencia;
      this.form.emergencia__id = this.emergencia;
      this.emergencia_bool = true
    } else if (this.$route.params.atendimento != null) {
      this.atendimento = this.$route.params.atendimento;
      this.form.atendimento__id = this.atendimento;
      this.atendimento_bool = true
    }
    if (this.$route.params.id != null) {
      this.pk = this.$route.params.id;
      this.editar();
    }
  },
  watch: {}
});
</script>

<style>
.col {
  margin: 1px;
}
</style>
