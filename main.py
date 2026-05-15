from reactpy import component, html, use_state, run

@component
def App():
    # Estados para o formulário
    nome, set_nome = use_state("")
    nota1, set_nota1 = use_state("")
    nota2, set_nota2 = use_state("")
    
    # Estado para a lista de alunos (nosso banco de dados)
    banco_dados_alunos, set_banco_dados_alunos = use_state([])
    erro, set_erro = use_state("") # Começa vazio
    def adicionar_aluno(event):
        # Validação simples
        try:
            n1 = float(nota1)
            n2 = float(nota2)
            if not (0 <= n1 <= 10 and 0 <= n2 <= 10):
                set_erro("As notas devem estar entre 0 e 10!")
                return
        except ValueError:
            set_erro("Por favor, digite apenas números!")
            return

        media = (n1 + n2) / 2
        
        # Lógica de situação
        if media >= 7.0: situacao = "APROVADO"
        elif media >= 5.0: situacao = "RECUPERAÇÃO"
        else: situacao = "REPROVADO"

        novo_aluno = {
            "nome": nome,
            "media": round(media, 1),
            "situacao": situacao
        }

        # Atualiza a lista (spread operator style)
        set_banco_dados_alunos([*banco_dados_alunos, novo_aluno])
        
        # Limpa os campos
        set_nome("")
        set_nota1("")
        set_nota2("")

    # Estilização com Bootstrap via CDN
    return html.div(
        html.head(
            html.link({
                "rel": "stylesheet",
                "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
            })
        ),
        html.div({"className": "container mt-5"},
        html.h1({"className": "text-center mb-4"}, "Sistema Escolar"),

    # SÓ EXIBE SE O ESTADO 'ERRO' NÃO ESTIVER VAZIO
        html.div({"className": f"alert alert-danger {'d-none' if not erro else ''}"}, 
        erro
    ),
            
            # Formulário Responsivo
            html.div({"className": "card p-4 shadow-sm mb-5"},
                html.div({"className": "row g-3"},
                    html.div({"className": "col-md-4"},
                        html.input({
                            "className": "form-control",
                            "placeholder": "Nome do Aluno",
                            "value": nome,
                            "on_change": lambda event: set_nome(event["target"]["value"])
                        })
                    ),
                    html.div({"className": "col-md-3"},
                        html.input({
                            "type": "number",
                            "className": "form-control",
                            "placeholder": "Nota 1",
                            "value": nota1,
                            "on_change": lambda event: set_nota1(event["target"]["value"])
                        })
                    ),
                    html.div({"className": "col-md-3"},
                        html.input({
                            "type": "number",
                            "className": "form-control",
                            "placeholder": "Nota 2",
                            "value": nota2,
                            "on_change": lambda event: set_nota2(event["target"]["value"])
                        })
                    ),
                    html.div({"className": "col-md-2 d-grid"},
                        html.button({
                            "className": "btn btn-primary",
                            "on_click": adicionar_aluno
                        }, "Cadastrar")
                    )
                )
            ),

            # Tabela de Resultados
            html.div({"className": "table-responsive"},
                html.table({"className": "table table-hover border"},
                    html.thead({"className": "table-dark"},
                        html.tr(
                            html.th("Aluno"),
                            html.th("Média"),
                            html.th("Situação")
                        )
                    ),
                    html.tbody(
                        [html.tr({"key": i},
                            html.td(aluno["nome"]),
                            html.td(aluno["media"]),
                            html.td({
                                "className": f"fw-bold {'text-success' if aluno['situacao'] == 'APROVADO' else 'text-warning' if aluno['situacao'] == 'RECUPERAÇÃO' else 'text-danger'}"
                            }, aluno["situacao"])
                        ) for i, aluno in enumerate(banco_dados_alunos)]
                    )
                )
            ),
            
            # Resumo Estatístico (Card debaixo)
            html.div({"className": "mt-4 p-3 bg-light border rounded"},
                html.p({"className": "mb-0"}, f"Total de Alunos: {len(banco_dados_alunos)}"),
                html.p({"className": "mb-0"}, f"Média Geral: {round(sum(a['media'] for a in banco_dados_alunos)/len(banco_dados_alunos), 1) if banco_dados_alunos else 0}")
            )
        )
    )

if __name__ == "__main__":
    run(App)