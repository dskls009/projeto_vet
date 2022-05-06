<template>
  <q-page padding class="full-width">
    <div class="q-pa-md" v-show="busca">
      <div class="q-pa-md">
        <q-table
          title="Tutores"
          :data="data_tutor"
          :columns="columns_tutor"
          :pagination.sync="pagination"
          :loading="loading_tutor"
          class="full-width"
          :rows-per-page-options="[0]"
          virtual-scroll
          binary-state-sort
          style="max-height: 400px;"
          separator="cell"
          dense
        >
          <template v-slot:top-right>
            <q-input
              borderless
              dense
              debounce="300"
              v-model="filtro_tutor"
              @input="load_tutor"
            >
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </template>
          <template v-slot:body="props">
            <tr :props="props">
              <q-td :props="props" key="cpf">{{ props.row.cpf }} </q-td>
              <q-td :props="props" key="nome">{{ props.row.nome }} </q-td>
              <q-td :props="props" key="sobrenome"
                >{{ props.row.sobrenome }}
              </q-td>
              <q-td :props="props" key="email">{{ props.row.email }} </q-td>
              <q-td :props="props" key="telefone_1"
                >{{ props.row.telefone_1 }}
              </q-td>
              <q-td :props="props" key="telefone_2"
                >{{ props.row.telefone_2 }}
              </q-td>
              <q-td :props="props" key="animais">
                <q-btn
                  size="sm"
                  dense
                  icon="pets"
                  flat
                  color="primary"
                  rounded
                  @click="ver_animais(props.row)"
                ></q-btn>
              </q-td>
            </tr>
          </template>
        </q-table>
      </div>
      <div class="q-pa-md">
        <q-table
          title="Animais"
          :data="data_animal"
          :columns="columns_animal"
          :pagination.sync="pagination"
          :loading="loading_animal"
          class="full-width"
          :rows-per-page-options="[0]"
          virtual-scroll
          binary-state-sort
          style="max-height: 400px;"
          separator="cell"
          dense
        >
          <template v-slot:top-right>
            <q-input
              borderless
              dense
              debounce="300"
              v-model="filtro_animal"
              @input="load_animal"
            >
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </template>
          <template v-slot:body="props">
            <tr :props="props">
              <q-td :props="props" key="rga">{{ props.row.rga }} </q-td>
              <q-td :props="props" key="nome">{{ props.row.nome }} </q-td>
              <q-td :props="props" key="especie">{{ props.row.especie }} </q-td>
              <q-td :props="props" key="raca">{{ props.row.raca }} </q-td>
              <q-td :props="props" key="cor">{{ props.row.cor }} </q-td>
              <q-td :props="props" key="nascimento"
                >{{ props.row.nascimento }}
              </q-td>
              <q-td :props="props" key="peso">{{ props.row.peso }} </q-td>
              <q-td :props="props" key="porte">{{ props.row.porte }} </q-td>
              <q-td :props="props" key="castrado"
                >{{ props.row.castrado ? 'Castrado' : '' }}
              </q-td>
              <q-td :props="props" key="info">
                <q-btn
                  size="sm"
                  dense
                  icon="pets"
                  flat
                  color="primary"
                  rounded
                  @click="ver_informacoes(props.row)"
                ></q-btn>
              </q-td>
            </tr>
          </template>
        </q-table>
      </div>
    </div>
    <div class="q-pa-md" v-show="!busca">
      <div class="q-pa-md">
        <q-btn
          round
          flat
          color="primary"
          icon="arrow_back"
          @click="busca = true"
        />
      </div>
      <div class="row">
        <div class="col">
          <q-input readonly filled v-model="form.rga" label="RGA" dense/>
        </div>
        <div class="col">
          <q-input readonly filled v-model="form.nome" label="Nome" dense/>
        </div>
        <div class="col">
          <q-input
            readonly
            filled
            label="Castrado"
            :value="form.castrado ? 'Sim' : 'Não'"
            dense
          />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-input readonly filled v-model="form.especie" label="Espécie" dense/>
        </div>
        <div class="col">
          <q-input readonly filled v-model="form.raca" label="Raça" dense/>
        </div>
        <div class="col">
          <q-input readonly filled v-model="form.cor" label="Cor" dense/>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <q-input
            readonly
            filled
            v-model="form.nascimento"
            label="Nascimento"
            type="date"
            dense
          />
        </div>
        <div class="col">
          <q-input readonly filled v-model="form.peso" label="Peso" dense/>
        </div>
        <div class="col">
          <q-input readonly filled v-model="form.porte" label="Porte" dense/>
        </div>
      </div>
      <div class="row">
        <div class="col-12 q-pa-md">
          <q-table
            title="Histórico"
            :data="data_consulta"
            :columns="columns_consulta"
            :pagination.sync="pagination"
            :loading="loading_consulta"
            class="full-width"
            :rows-per-page-options="[0]"
            virtual-scroll
            binary-state-sort
            style="max-height: 400px;"
            separator="cell"
            dense
          >
            <template v-slot:top-right>
              <q-input
                borderless
                dense
                debounce="300"
                v-model="filtro_consulta"
                @input="load_consulta"
              >
                <template v-slot:append>
                  <q-icon name="search" />
                </template>
              </q-input>
            </template>
            <template v-slot:body="props">
              <tr :props="props">
                <q-td :props="props" key="descricao"
                  >{{ props.row.descricao }}
                </q-td>
                <q-td :props="props" key="observacao"
                  >{{ props.row.observacao }}
                </q-td>
                <q-td :props="props" key="info">
                <q-btn
                  size="sm"
                  dense
                  icon="pets"
                  flat
                  color="primary"
                  rounded
                  @click="ver_vac_med(props.row)"
                ></q-btn>
              </q-td>
              </tr>
            </template>
          </q-table>
        </div>
      </div>
      <div class="row">
        <div class="col-6 q-pa-md">
          <q-table
            title="Vacinas"
            :data="data_vacina"
            :columns="columns_vacina"
            :pagination.sync="pagination"
            :loading="loading_vacina"
            class="full-width"
            :rows-per-page-options="[0]"
            virtual-scroll
            binary-state-sort
            style="max-height: 400px;"
            separator="cell"
            dense
          >
            <template v-slot:top-right>
              <q-input
                borderless
                dense
                debounce="300"
                v-model="filtro_vacina"
                @input="load_vacina"
              >
                <template v-slot:append>
                  <q-icon name="search" />
                </template>
              </q-input>
            </template>
            <template v-slot:body="props">
              <tr :props="props">
                <q-td :props="props" key="vacina"
                  >{{ props.row.descricao }}
                </q-td>
                <q-td :props="props" key="dose">{{ props.row.dose }} </q-td>
                <q-td :props="props" key="data_aplicacao"
                  >{{ props.row.data_aplicacao }}
                </q-td>
                <q-td :props="props" key="proxima_dose"
                  >{{ props.row.proxima_dose }}
                </q-td>
                <q-td :props="props" key="observacao"
                  >{{ props.row.observacao }}
                </q-td>
              </tr>
            </template>
          </q-table>
        </div>
        <div class="col-6 q-pa-md">
          <q-table
            title="Medicamentos"
            :data="data_medicamento"
            :columns="columns_medicamento"
            :pagination.sync="pagination"
            :loading="loading_medicamento"
            class="full-width"
            :rows-per-page-options="[0]"
            virtual-scroll
            binary-state-sort
            style="max-height: 400px;"
            separator="cell"
            dense
          >
            <template v-slot:top-right>
              <q-input
                borderless
                dense
                debounce="300"
                v-model="filtro_medicamento"
                @input="load_medicamento"
              >
                <template v-slot:append>
                  <q-icon name="search" />
                </template>
              </q-input>
            </template>
            <template v-slot:body="props">
              <tr :props="props">
                <q-td :props="props" key="medicamento"
                  >{{ props.row.medicamento }}
                </q-td>
                <q-td :props="props" key="quantidade"
                  >{{ props.row.quantidade }}
                </q-td>
                <q-td :props="props" key="observacao"
                  >{{ props.row.observacao }}
                </q-td>
              </tr>
            </template>
          </q-table>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { findall as tutor_findall } from '../../services/commons/ClienteService';
import { findall as animal_findall } from '../../services/commons/AnimalService';
import { findall as consulta_findall } from '../../services/veterinaria/ConsultaService';
import { findall as vacina_findall } from '../../services/veterinaria/VacinaService';
import { findall as medicamento_findall } from '../../services/veterinaria/MedicamentoService';

export default {
  name: 'BuscaView',
  data() {
    return {
      // props: {},
      form: {},
      busca: true,
      tutor: '',
      animal: '',
      filtro_tutor: undefined,
      filtro_animal: undefined,
      filtro_consulta: undefined,
      filtro_vacina: undefined,
      filtro_medicamento: undefined,
      pagination: {
        sortBy: 'desc',
        descending: false,
        rowsPerPage: 0
      },
      data_tutor: [],
      data_animal: [],
      data_consulta: [],
      data_vacina: [],
      data_medicamento: [],
      loading_animal: false,
      loading_tutor: false,
      loading_consulta: false,
      loading_vacina: false,
      loading_medicamento: false,
      columns_tutor: [
        {
          name: 'cpf',
          label: 'CPF',
          align: 'left',
          sortable: false
        },
        {
          name: 'nome',
          label: 'Nome',
          align: 'left',
          sortable: true
        },
        {
          name: 'sobrenome',
          label: 'Sobrenome',
          align: 'left',
          sortable: true
        },
        {
          name: 'email',
          label: 'Email',
          align: 'left',
          sortable: true
        },
        {
          name: 'telefone_1',
          label: 'Telefone (1)',
          align: 'left',
          sortable: false
        },
        {
          name: 'telefone_2',
          label: 'Telefone (2)',
          align: 'left',
          sortable: false
        },
        {
          name: 'animais',
          label: 'Animais',
          align: 'center',
          sortable: false
        }
      ],
      columns_animal: [
        {
          name: 'rga',
          label: 'RGA',
          align: 'left',
          sortable: false
        },
        {
          name: 'nome',
          label: 'Nome',
          align: 'left',
          sortable: true
        },
        {
          name: 'especie',
          label: 'Espécie',
          align: 'left',
          sortable: true
        },
        {
          name: 'raca',
          label: 'Raça',
          align: 'left',
          sortable: true
        },
        {
          name: 'cor',
          label: 'Cor',
          align: 'left',
          sortable: false
        },
        {
          name: 'nascimento',
          label: 'Data de Nascimento',
          align: 'left',
          sortable: false
        },
        {
          name: 'peso',
          label: 'Peso',
          align: 'left',
          sortable: false
        },
        {
          name: 'porte',
          label: 'Porte',
          align: 'left',
          sortable: false
        },
        {
          name: 'castrado',
          label: 'Castrado',
          align: 'left',
          sortable: false
        },
        {
          name: 'info',
          label: 'Informações',
          align: 'center',
          sortable: false
        }
      ],
      columns_consulta: [
        {
          name: 'descricao',
          label: 'Descrição',
          align: 'left',
          sortable: false
        },
        {
          name: 'observacao',
          label: 'Observação',
          align: 'left',
          sortable: true
        },
        {
          name: 'info',
          label: 'Informações',
          align: 'center',
          sortable: false
        }
      ],
      columns_vacina: [
        {
          name: 'vacina',
          label: 'Vacina',
          align: 'left',
          sortable: false
        },
        {
          name: 'dose',
          label: 'Dose',
          align: 'left',
          sortable: true
        },
        {
          name: 'data_aplicacao',
          label: 'Data de Aplicação',
          align: 'left',
          sortable: true
        },
        {
          name: 'proxima_dose',
          label: 'Próxima Dose',
          align: 'left',
          sortable: true
        },
        {
          name: 'observacao',
          label: 'Observação',
          align: 'left',
          sortable: true
        }
      ],
      columns_medicamento: [
        {
          name: 'medicamento',
          label: 'Medicamento',
          align: 'left',
          sortable: false
        },
        {
          name: 'quantidade',
          label: 'Quantidade',
          align: 'left',
          sortable: true
        },
        {
          name: 'observacao',
          label: 'Observação',
          align: 'left',
          sortable: true
        }
      ]
    };
  },
  methods: {
    ver_animais: function(row) {
      this.tutor = row.id + '';
      animal_findall(this);
    },
    ver_informacoes: function(row) {
      this.form = row;
      this.animal = row.id + '';
      consulta_findall(this);
      this.busca = false;
    },
    ver_vac_med: function(row) {
      this.consulta = row.id + '';
      vacina_findall(this);
      medicamento_findall(this);
    },
    load_tutor: function() {
      tutor_findall(this);
    },
    load_animal: function() {
      animal_findall(this);
    },
    load_consulta: function() {
      consulta_findall(this);
    },
    load_vacina: function() {
      vacina_findall(this);
    },
    load_medicamento: function() {
      medicamento_findall(this);
    }
  },
  mounted: function() {
    this.load_tutor();
    console.log(this.$route.params.id)
  }
};
</script>
