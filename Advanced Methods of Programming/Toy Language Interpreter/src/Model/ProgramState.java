package Model;

import Model.Containers.*;
import Model.Statements.IStatement;
import Util.Pair;

import java.io.BufferedReader;

public class ProgramState {
    private MyIStack<IStatement> exeStack;
    private MyIDictionary<String, Integer> symTable;
    private MyIFileTable<Pair<String, BufferedReader>> fileTable;
    private MyIHeap<Integer> heap;
    private String output;

    public ProgramState(){
        exeStack  = new MyStack<>();
        symTable  = new MyDictionary<>();
        fileTable = new MyFileTable<>();
        heap      = new MyHeap<>();
        output    = "";
    }

    public MyIHeap<Integer> getHeap() {
        return heap;
    }

    public void setHeap( MyIHeap<Integer> heap ){
        this.heap = heap;
    }

    public MyIStack<IStatement> getExeStack() {
        return exeStack;
    }

    public void setExeStack( MyIStack<IStatement> exeStack ){
        this.exeStack = exeStack;
    }

    public void setExeStack( IStatement statement ) {
        MyIStack<IStatement> newStack = new MyStack<>();
        newStack.push(statement);
        this.exeStack = newStack;
    }
    public MyIDictionary<String, Integer> getSymTable() {
        return symTable;
    }

    public void setSymTable( MyIDictionary<String, Integer> symTable ){
        this.symTable = symTable;
    }

    public MyIFileTable<Pair<String, BufferedReader>> getFileTable() {
        return fileTable;
    }

    public void setFileTable(MyIFileTable<Pair<String, BufferedReader>> fileTable){
        this.fileTable = fileTable;
    }

    public String getOutput() {
        return output;
    }

    public void setOutput(String output) {
        this.output = output;
    }

    public void appendOutput(String s){
        this.output = this.output + s;
    }

    public String toString(){
        return "ExeStack:\n" + exeStack.toString() +
                "SymLink:\n" + symTable.toString() +
                "FileTable:\n" + fileTable.toString() +
                "Heap:\n" + heap.toString() +
                "Output:\n" + output;
    }

}
