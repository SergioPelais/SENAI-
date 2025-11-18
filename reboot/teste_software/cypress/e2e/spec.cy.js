describe('teste de login', () => {
  it('logado com sucesso', () => {
    cy.visit('http://127.0.0.1:5000/')
    cy.get('[name="nif"]').type('2345678');
    cy.get('[name="senha"]').type('1234');
    cy.get('#btnform').click(); 
  })
  it('login invalido', () => {
    cy.visit('http://127.0.0.1:5000/')
    cy.get('[name="nif"]').type('7654321');
    cy.get('[name="senha"]').type('4321');
    cy.get('#btnform').click(); 
  })
  it('logado com cookie', () => {
    cy.visit('http://127.0.0.1:5000/')
    cy.get('[name="nif"]').type('1234567');
    cy.get('[name="senha"]').type('1234');
    cy.get('[name="lembrar"]').check();
    cy.get('#btnform').click(); 
  })
  it.only('login bloqueado', () => {
    cy.visit('http://127.0.0.1:5000/')
    cy.get('[name="nif"]').type('1234567');
    cy.get('[name="senha"]').type('4321');
    cy.get('#btnform').click(); 
    cy.get('[name="nif"]').type('1234567');
    cy.get('[name="senha"]').type('4321');
    cy.get('#btnform').click(); 
    cy.get('[name="nif"]').type('1234567');
    cy.get('[name="senha"]').type('4321');
    cy.get('#btnform').click(); 
    cy.get('[name="nif"]').type('1234567');
    cy.get('[name="senha"]').type('4321');
    cy.get('#btnform').click(); 
    cy.get('[name="nif"]').type('1234567');
    cy.get('[name="senha"]').type('4321');
    cy.get('#btnform').click(); 
  })
  it('logout', () => {
    cy.visit('http://127.0.0.1:5000/')
    cy.get('[name="nif"]').type('1234567');
    cy.get('[name="senha"]').type('1234');
    cy.get('#btnform').click();
    cy.get('#btn-menu img').click();
    cy.get('#sair-login').click();
  })
})

describe('teste de login', () => {

})