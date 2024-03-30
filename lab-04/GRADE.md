Dear Student,

I'm happy to announce that you've managed to get **5** out of 10 points for this assignment.
<details><summary>You have already managed to pass 4 tests, so that is encouraging!</summary>&emsp;☑&nbsp;[1p] Maximization problem should be converted to minimization problem<br>&emsp;☑&nbsp;[1p] Rectangular problem should be padded with constant to make it square<br>&emsp;☑&nbsp;[2p] Simplex should be able to solve assignment problems<br>&emsp;☑&nbsp;[1p] Should subtract min values in every row and column in cost matrix</details>

There still exist some issues that should be addressed before the deadline: **2023-05-17 07:59:00 CEST (+0200)**. For further details, please refer to the following list:

<details><summary>[2p] Should find partial assignment in cost matrix &gt;&gt; partial assignment is incorrect:</summary>- got: {}<br>- got assignment for only 0 workers, expected to assign tasks to 3 workers<br>- for cost matrix: <br>&nbsp;&nbsp;&nbsp;&nbsp;[[0 3 4]<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[1 0 0]<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[3 3 0]]</details>
<details><summary>[2p] Should perform crossing algorithm on cost matrix &gt;&gt; Tested code raises NotImplementedError in hungarian_solver.py:57</summary></details>
<details><summary>[1p] Should create proper assignment based on dict of assignments &gt;&gt; hungarian algorithm returns incorrect objective:</summary>- got: None<br>- expected: 12<br>- for cost matrix: <br>&nbsp;&nbsp;&nbsp;&nbsp;[[4 9 8]<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[6 7 5]<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4 6 1]]<br>- and assignment: None</details>

-----------
I remain your faithful servant\
_Bobot_