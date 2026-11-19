from app.services import filmes_service

filmes = filmes_service.listar_filmes()
generos = filmes_service.listar_generos()

print("FILMES:")
for filme in filmes:
    print(filme["titulo"])

print("\nGÊNEROS:")
for genero in generos:
    print(genero["nome"])