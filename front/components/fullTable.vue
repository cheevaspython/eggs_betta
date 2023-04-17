<template>
  <table class="table">
    <tr class="table__title">
      <td>Категория</td>
      <td>Кол-во (дес.)</td>
      <td>Цена</td>
    </tr>
    <tr>
      <td>CB</td>
      <td>{{ app.cB }}</td>
      <td>{{ app.cB_cost }} ₽</td>
    </tr>
    <tr>
      <td>C0</td>
      <td>{{ app.c0 }}</td>
      <td>{{ app.c0_cost }} ₽</td>
    </tr>
    <tr>
      <td>C1</td>
      <td>{{ app.c1 }}</td>
      <td>{{ app.c1_cost }} ₽</td>
    </tr>
    <tr>
      <td>C2</td>
      <td>{{ app.c2 }}</td>
      <td>{{ app.c2_cost }} ₽</td>
    </tr>
    <tr>
      <td>C3</td>
      <td>{{ app.c3 }}</td>
      <td>{{ app.c3_cost }} ₽</td>
    </tr>
    <tr>
      <td>Грязь</td>
      <td>{{ app.dirt }}</td>
      <td>{{ app.dirt_cost }} ₽</td>
    </tr>
  </table> 
</template>

<script>
 export default {
  name: "fullTable",
  props: ['app']
}
</script>

<style lang="scss" scoped>
.table {
  text-align: center;
  border: solid #ebebeb 3px; 
  margin-bottom: 1rem;

  &__title {
    background-color: #f5f5f5;
  }
}

td {
  font-weight: 400;
}
</style>