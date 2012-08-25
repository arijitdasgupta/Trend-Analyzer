Trend Analyzer
==============

The program
-----------

The programs are meant to predict trends in multidimensional datasets. If you have a data set with parameters more than three there will be difficulties visualizing it. That's why these two programs are made, to help visualizing the data set but not producing a graph, but predicting regions or scalar values in the other points in the multidimensional space. Both program fundamentally uses the same method to produce the prediction outputs.

There are two programs here stored in this repository,

1. Discrete Trend Analyzer

2. Scalar Trend Analyzer

1. Discrete Trend Analyzer
--------------------------

This program can be used to treat data-set where there are discrete qualitative outcomes associated with each point in the parameter space. It accepts a table of data, where there are columns for parameters, and columns for discrete properties. The program will generate outputs for each columns of discrete properties and for each discrete property, leaving the points that is already in the data-set. And it will also generate a file for each discrete property columns, where there will be a list of predicted points of interest, or the points where the predictions are most prone to get wrong (The edge of the discrete property regions).

2. Scalar Trend Analyzer
------------------------

Similar to the previous program, this program accept data-sets where there is a scalar value associated with each point in parameter space. And then the program tries to make a comparative prediction of where the scalar over the whole parameter space. This program also accepts a table with columns for each scalar values of interest and gives chart of predicted scalar values of each scalar columns of interest.

How to use
----------

The program accepts standard comma separated value (CSV) tables. Make sure your table is properly filled and aligned, otherwise erroes will arise, which are handled gracefully in the program via exceptiopn handling and capture. But the current version of the programs will be unable to detect the cause of the problem.

There are custom command line options with default settings. If one is providing command line options, he/she has to provide all the command line options, for both the programs.

```
1. Discrete Trend Analyzer.py
```

Command line options are as follows, each option accepts a value

```
-f, --filename => The data filename.
-t, --textrow => The row for the table fields (the top-most row), starts with zero (first row) by default.
-n, --numberrow => The row from which the data starts, start with 2 by default. Row numbering starts from 0.
-u, --ucolumn => The columns that are used as parameter columns. Provide multiple times with a number for multiple parameters.
-d, --ducolumn => The column containing the discrete properties. Provide multiple times with a number for multiple property columns.
-r, --reso => The resolution of analysis. The less the resolution, the faster it the program will be.
```

```
2. Scalar Trend Analyzer.py
```

Command line options are almost as same as before,

```
-f, --filename => The data filename.
-t, --textrow => The row for the table fields (the top-most row), starts with zero (first row) by default.
-n, --numberrow => The row from which the data starts, start with 2 by default. Row numbering starts from 0.
```

The only changes are,

```
-p, --parameter => To specify a parameter column on the table.
-s, --scalar => To specify a scalar column of interest in the table.
-r, --resolution => The resolution of analysis. The less the resolution, the faster it the program will be.
```

Both the program will run on Python Standard Library. Python 2.6.2 recommended.

Last words
----------

The first program, i.e. Discrete Trend Analyzer.py is tested with test case simulation and works fine. The second program is not yet simulation tested.

Any feedback, comment is welcome. Feel free to look into the code.

P.S. This README is written in a hurry, please do tell me if something needs clarification.
