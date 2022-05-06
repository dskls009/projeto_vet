import { RouteConfig } from 'vue-router';


const routes: RouteConfig[] = [
  {
    path: '/login',
    component: () => import('pages/commons/LoginView.vue')
  },
  {
    path: '',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: '/cliente/busca', component: () => import('pages/commons/ClienteBuscaView.vue') },
      { path: '/cliente/cadastro', component: () => import('pages/commons/ClienteCadastroView.vue') },
      { path: '/cliente/edicao/:id', component: () => import('pages/commons/ClienteCadastroView.vue') },
      { path: '/animal/busca', component: () => import('pages/commons/AnimalBuscaView.vue') },
      { path: '/animal/busca/:cliente', component: () => import('pages/commons/AnimalBuscaView.vue') },
      { path: '/animal/cadastro', component: () => import('pages/commons/AnimalCadastroView.vue') },
      { path: '/animal/cadastro/:cliente', component: () => import('pages/commons/AnimalCadastroView.vue') },
      { path: '/animal/edicao/:id', component: () => import('pages/commons/AnimalCadastroView.vue') },
      { path: '/consulta/busca', component: () => import('pages/veterinaria/ConsultaBuscaView.vue') },
      { path: '/consulta/busca/:animal', component: () => import('pages/veterinaria/ConsultaBuscaView.vue') },
      { path: '/consulta/cadastro/:animal', component: () => import('pages/veterinaria/ConsultaCadastroView.vue') },
      { path: '/consulta/edicao/:animal/:id', component: () => import('pages/veterinaria/ConsultaCadastroView.vue') },
      { path: '/cirurgia/busca', component: () => import('pages/veterinaria/CirurgiaBuscaView.vue') },
      { path: '/cirurgia/busca/:animal', component: () => import('pages/veterinaria/CirurgiaBuscaView.vue') },
      { path: '/cirurgia/cadastro/:animal', component: () => import('pages/veterinaria/CirurgiaCadastroView.vue') },
      { path: '/cirurgia/edicao/:animal/:id', component: () => import('pages/veterinaria/CirurgiaCadastroView.vue') },
      { path: '/emergencia/busca', component: () => import('pages/veterinaria/EmergenciaBuscaView.vue') },
      { path: '/emergencia/busca/:animal', component: () => import('pages/veterinaria/EmergenciaBuscaView.vue') },
      { path: '/emergencia/cadastro/:animal', component: () => import('pages/veterinaria/EmergenciaCadastroView.vue') },
      { path: '/emergencia/edicao/:animal/:id', component: () => import('pages/veterinaria/EmergenciaCadastroView.vue') },
      { path: '/atendimento/busca', component: () => import('pages/veterinaria/AtendimentoBuscaView.vue') },
      { path: '/atendimento/busca/:animal', component: () => import('pages/veterinaria/AtendimentoBuscaView.vue') },
      { path: '/atendimento/cadastro/:animal', component: () => import('pages/veterinaria/AtendimentoCadastroView.vue') },
      { path: '/atendimento/edicao/:animal/:id', component: () => import('pages/veterinaria/AtendimentoCadastroView.vue') },
      { path: '/medicamento/busca', component: () => import('pages/veterinaria/MedicamentoBuscaView.vue') },
      { path: '/medicamento/cadastro', component: () => import('pages/veterinaria/MedicamentoCadastroView.vue') },
      { path: '/medicamento/edicao/:id', component: () => import('pages/veterinaria/MedicamentoCadastroView.vue') },
      { path: '/doenca/busca', component: () => import('pages/veterinaria/DoencaBuscaView.vue') },
      { path: '/doenca/cadastro', component: () => import('pages/veterinaria/DoencaCadastroView.vue') },
      { path: '/doenca/edicao/:id', component: () => import('pages/veterinaria/DoencaCadastroView.vue') },
      { path: '/receituario/busca', component: () => import('pages/veterinaria/ReceituarioBuscaView.vue') },
      { path: '/receituario/cadastro', component: () => import('pages/veterinaria/ReceituarioCadastroView.vue') },
      { path: '/receituario/edicao/:id', component: () => import('pages/veterinaria/ReceituarioCadastroView.vue') },
      { path: '/medicamento_administrado/busca/consulta/:consulta', component: () => import('pages/veterinaria/MedicamentoAdministradoBuscaView.vue') },
      { path: '/medicamento_administrado/cadastro/consulta/:consulta', component: () => import('pages/veterinaria/MedicamentoAdministradoCadastroView.vue') },
      { path: '/medicamento_administrado/edicao/consulta/:consulta/:id', component: () => import('pages/veterinaria/MedicamentoAdministradoCadastroView.vue') },
      { path: '/medicamento_administrado/busca/cirurgia/:cirurgia', component: () => import('pages/veterinaria/MedicamentoAdministradoBuscaView.vue') },
      { path: '/medicamento_administrado/cadastro/cirurgia/:cirurgia', component: () => import('pages/veterinaria/MedicamentoAdministradoCadastroView.vue') },
      { path: '/medicamento_administrado/edicao/cirurgia/:cirurgia/:id', component: () => import('pages/veterinaria/MedicamentoAdministradoCadastroView.vue') },
      { path: '/medicamento_administrado/busca/emergencia/:emergencia', component: () => import('pages/veterinaria/MedicamentoAdministradoBuscaView.vue') },
      { path: '/medicamento_administrado/cadastro/emergencia/:emergencia', component: () => import('pages/veterinaria/MedicamentoAdministradoCadastroView.vue') },
      { path: '/medicamento_administrado/edicao/emergencia/:emergencia/:id', component: () => import('pages/veterinaria/MedicamentoAdministradoCadastroView.vue') },
      { path: '/medicamento_administrado/busca/atendimento/:atendimento', component: () => import('pages/veterinaria/MedicamentoAdministradoBuscaView.vue') },
      { path: '/medicamento_administrado/cadastro/atendimento/:atendimento', component: () => import('pages/veterinaria/MedicamentoAdministradoCadastroView.vue') },
      { path: '/medicamento_administrado/edicao/atendimento/:atendimento/:id', component: () => import('pages/veterinaria/MedicamentoAdministradoCadastroView.vue') },
      { path: '/vacina/busca', component: () => import('pages/veterinaria/VacinaBuscaView.vue') },
      { path: '/vacina/busca/:animal', component: () => import('pages/veterinaria/VacinaBuscaView.vue') },
      { path: '/vacina/cadastro/:animal', component: () => import('pages/veterinaria/VacinaCadastroView.vue') },
      { path: '/vacina/edicao/:animal/:id', component: () => import('pages/veterinaria/VacinaCadastroView.vue') },
      { path: '/relatorios/cliente', component: () => import('pages/relatorios/ClienteRelatorioView.vue')}
    ]
  },
  

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
];

export default routes;
