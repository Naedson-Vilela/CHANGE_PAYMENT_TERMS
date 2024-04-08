import time
import flet as ft
import app



def main(page: ft.Page):
    
    
    page.window_height = 400
    page.window_width = 750
    page.window_resizable = False
    page.title = 'Alterar Condições de Pagamento'
    page.window_center()
    
    mapas = []
    
    # DEFININDO CONTROLS 
    
    def pick_arquivo(e:ft.FilePickerResultEvent):
        for x in e.files:
            caminho_arquivo_text.value = x.name
            caminho_arquivo = x.path
            app.data = app.carregar_arquivo(caminho_arquivo)
            caminho_arquivo_text.update()
        condicao_old_dropdown.options, condicao_new_dropdown.options = app.get_condicoes_options(((revenda_dropdown.value).upper()).replace(' ', '_'))
        mapa_dropdown.options = app.get_mapas_options()
        upload_arquivo_button.disabled = False
        page.update()
    
    pick_file = ft.FilePicker(on_result=pick_arquivo)
    page.overlay.append(pick_file)
    
    caminho_arquivo_text = ft.TextField(
        read_only=True,
        label='Caminho do Arquivo',
        value='...',
        color="#333333",
        width=350,
        disabled=True
        )
    
    porcentagem_text = ft.Text('Clique em "Iniciar" para começar as alterações', size=20)
    
    upload_arquivo_button = ft.FloatingActionButton(
        content=ft.Text('Upload'),
        width=100,
        on_click=lambda _: pick_file.pick_files(),
        )
    
    upload_arquivo_button.disabled = True
    
    def validar_escolha(e):
        if condicao_new_dropdown.value and condicao_new_dropdown.value and mapa_dropdown.value:
            iniciar_button.disabled=False
            
            page.update()
        
    
    mapa_dropdown = ft.Dropdown(
        label='Mapas',
        options=mapas,
        width=200,
        on_change=validar_escolha
    )
    condicao_old_dropdown = ft.Dropdown(
        label='Antiga Condição',
        width=245,
        on_change=validar_escolha
    )
    condicao_new_dropdown = ft.Dropdown(
        label='Nova Condição',
        width=245,
        on_change=validar_escolha
    )
    def get_options(e):
        upload_arquivo_button.disabled = False
        page.update()
    
    def exibir_contador(cont):
        porcentagem_text.value = f'Iniciando em {cont}...'
        page.update()
        time.sleep(1)
        if cont==1:
            porcentagem_text.value = f'Progresso: 00.00%'
            page.update()

    
    def resetar_estado():
        caminho_arquivo_text.value = '...'
        mapa_dropdown.options = []
        condicao_old_dropdown.options = []
        condicao_new_dropdown.options = []
        iniciar_button.disabled = True
        cancelar_button.disabled = True
        revenda_dropdown.disabled = False
        mapa_dropdown.disabled = False
        condicao_old_dropdown.disabled = False
        condicao_new_dropdown.disabled = False
        porcentagem_text.value = 'Clique em "Iniciar" para começar as alterações'
        page.update()  
    
    def iniciar(e):
        alteracoes = []
        if mapa_dropdown.value == 'TODOS':
            codigo = app.get_condicao_codigo(condicao_new_dropdown.value, ((revenda_dropdown.value).upper()).replace(' ', '_'))
            notas_alterar, linhas= app.separar_notas(condicao_old_dropdown.value)
            iniciar_button.disabled = True
            cancelar_button.disabled = False
            pausar_button.disabled = False
            revenda_dropdown.disabled = True
            mapa_dropdown.disabled = True
            condicao_old_dropdown.disabled = True
            condicao_new_dropdown.disabled = True
            page.update()
            
            # Exibindo o contador
            for cont in range(3, 0, -1):
                exibir_contador(cont)
            
            print(notas_alterar)
            
            for k, v  in notas_alterar.items():
                for i in v:
                    alteracoes.append([k, i, codigo])
                    
            app.executar_codigo(alteracoes, porcentagem_text)
            
    def get_porcentagem_text():
        return porcentagem_text    
    
    def cancelar(e):
        app.running = False
        resetar_estado()
        page.update()
                
                
    revenda_dropdown = ft.Dropdown(
        label="Revenda",    
        hint_text='Selecione a revenda',
        options=[
            ft.dropdown.Option('Serra Talhada'),
            ft.dropdown.Option('Arcoverde'),
            ft.dropdown.Option('Ceara'),
            ft.dropdown.Option('Salgueiro'),
            ft.dropdown.Option('Garanhuns'),      
        ],
        width=page.window_width*0.32,
        autofocus=True,
        on_change=get_options
    )
    
    log_text_field = ft.TextField(
        multiline=True,
        min_lines=3,
        max_lines=3,
        disabled=True,
        width=200
        
    )
    log_text_field.visible = False
    
    
    
    
    iniciar_button = ft.FloatingActionButton(
        text='Iniciar',
        width=100,
        on_click=iniciar,
        disabled=True
        )
    pausar_button = ft.FloatingActionButton(
        text='Pausar',
        width=100,
        )
    pausar_button.disabled = True
    
    cancelar_button = ft.FloatingActionButton(
        text='Cancelar',
        width=100,
        on_click=cancelar
        )
    cancelar_button.disabled = True
    
    botoes = ft.Row(
                            controls=[
                                iniciar_button,
                                # pausar_button,
                                cancelar_button
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            width=750
                            
                        )
    
    page.add(
        ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Container(
                        content=revenda_dropdown,
                        ),
                    ft.Container(
                        content=caminho_arquivo_text,
                        ),
                    ft.Container(
                        content=upload_arquivo_button,
                        ),
                ],
            ),
            ft.Row(
                controls=[
                    mapa_dropdown,
                    condicao_old_dropdown,
                    condicao_new_dropdown
                ]
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=porcentagem_text,
                        margin=30
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=botoes,
                    )
                ]
            )
        ]
    ))
    
    page.update()

ft.app(target=main)