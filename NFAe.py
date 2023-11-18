import tkinter as tk
from tkinter import messagebox


class NFAE:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def epsilon_closure(self, state):
        epsilon_closure = {state}
        stack = [state]

        while stack:
            current_state = stack.pop()
            # nếu có tồn tại trạng thái hiện tại thì gán cho transition giá trị đó, ngược lại là rỗng
            transitions_for_state = self.transitions.get(current_state, {})
            # Trả về giá trị tương ứng với phép chuyển epsilon, nếu không thì trả  về set rỗng
            epsilon_transitions = transitions_for_state.get('ε', set())
            # if not epsilon_transitions:  # Kiểm tra nếu không có phép chuyển epsilon
            #     continue
            # Duyệt qua tất cả trạng thái có thể chuyển được bằng epsilon từ trạng thái hiện tại
            for epsilon_transition_state in epsilon_transitions:
                # Kiểm tra trạng thái hiện tại đã có trong tập epsilon_closure chưa
                if epsilon_transition_state not in epsilon_closure:
                    epsilon_closure.add(epsilon_transition_state)
                    stack.append(epsilon_transition_state)

        return epsilon_closure

    def delta(self, state, symbol):
        transitions_for_state = self.transitions.get(state, {})
        symbol_transitions = transitions_for_state.get(symbol, set())
        print(f"Before e-CLOSURE of {state} is {symbol_transitions}")

        result = set()
        if symbol_transitions:
            temp_states = set()
            for s in symbol_transitions:
                temp_states.add(s)
            for s in temp_states:
                result.update(self.epsilon_closure(s))

        return result if result is not None else set()


    def is_string_accepted(self, input_string):
        current_states = self.epsilon_closure(self.start_state)
        print("Epsilon closure start state ", self.epsilon_closure(self.start_state))
        print("\n")
        for symbol in input_string:
            new_states = set()
            for state in current_states:
                new_states.update(self.delta(state, symbol))
                print(f"e-CLOSURE( {state} , {symbol}) => {new_states}")
            current_states = new_states
            print(f"State Set of '{symbol}' => '{current_states}' \n")

        return any(state in self.accept_states for state in current_states)


# Example Usage
# states = {'q0', 'q1', 'q2'}
# alphabet = {'0', '1', '2'}
# print(type(alphabet))
# transitions = {
#     'q0': {'0': {'q0'}, 'ε': {'q1'}},
#     'q1': {'1': {'q1'}, 'ε': {'q2'}},
#     'q2': {'2': {'q2'}}
# }
# start_state = 'q0'
# accept_states = {'q2'}

class NFAEBuilder:
    def __init__(self, master):
        self.master = master
        self.master.title("NFAε Builder")
        self.master.geometry('800x600')
        self.states = tk.StringVar()
        self.alphabet = tk.StringVar()
        self.transitions = tk.StringVar()
        self.start_state = tk.StringVar()
        self.accept_states = tk.StringVar()
        self.input_string = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.master, text="Demo xây dựng NFAε và kiểm tra chuỗi", font=('bold', 24))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.master, text="States (comma-separated):", font=20).grid(row=1, column=0, sticky=tk.E)
        tk.Entry(self.master, textvariable=self.states, width=80, font=20).grid(row=1, column=1, pady=8, ipady=10)

        # Alphabet input
        tk.Label(self.master, text="Alphabet (comma-separated):", font=20).grid(row=2, column=0, sticky=tk.E)
        tk.Entry(self.master, textvariable=self.alphabet, width=80, font=20).grid(row=2, column=1, pady=8, ipady=10)

        # Transitions input
        tk.Label(self.master, text="Transitions (comma-separated):", font=20).grid(row=3, column=0, sticky=tk.E)
        tk.Entry(self.master, textvariable=self.transitions, width=80, font=20).grid(row=3, column=1, pady=8, ipady=50)

        # Start state input
        tk.Label(self.master, text="Start State:", font=20).grid(row=4, column=0, sticky=tk.E)
        tk.Entry(self.master, textvariable=self.start_state, width=80, font=20).grid(row=4, column=1, pady=8, ipady=10)

        # Accept states input
        tk.Label(self.master, text="Accept States (comma-separated):", font=20).grid(row=5, column=0, sticky=tk.E)
        tk.Entry(self.master, textvariable=self.accept_states, width=80, font=20).grid(row=5, column=1, pady=8,
                                                                                       ipady=10)

        # Input string for testing
        tk.Label(self.master, text="Test String:", font=20).grid(row=6, column=0, sticky=tk.E)
        tk.Entry(self.master, textvariable=self.input_string, width=80, font=20).grid(row=6, column=1, pady=8, ipady=10)

        # Buttons
        tk.Button(self.master, text="Build NFAε", command=self.build_nfae).grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(self.master, text="Test String", command=self.test_string).grid(row=8, column=0, columnspan=2,
                                                                                  pady=10)

    def build_nfae(self):
        # Get input values
        states = [s.strip() for s in self.states.get().split(',')]
        alphabet = set([a.strip() for a in self.alphabet.get().split(',')])
        transitions_list = [t.strip() for t in self.transitions.get().split(',')]
        start_state = self.start_state.get().strip()
        accept_states = set([s.strip() for s in self.accept_states.get().split(',')])

        # Parse transitions
        transitions = {}
        for t in transitions_list:
            transition_parts = t.split(':')
            state_from, symbol, state_to = [part.strip() for part in transition_parts]
            if state_from not in transitions:
                transitions[state_from] = {}
            if symbol not in transitions[state_from]:
                transitions[state_from][symbol] = set()
            transitions[state_from][symbol].add(state_to)

        # Create NFAE object
        self.nfae = NFAE(states, alphabet, transitions, start_state, accept_states)

        # Display NFAε information
        print("States:", states)
        print("Alphabet:", alphabet)
        print("Transitions:", transitions)
        print("Start State:", start_state)
        print("Accept States:", accept_states)

    def test_string(self):
        if not hasattr(self, 'nfae'):
            messagebox.showinfo("Error", "NFAε not built yet. Please build NFAε first.")
            return

        test_string = self.input_string.get().strip()
        if self.nfae.is_string_accepted(test_string):
            messagebox.showinfo("Result", f"The string '{test_string}' is accepted by the NFAε.")
        else:
            messagebox.showinfo("Result", f"The string '{test_string}' is not accepted by the NFAε.")


# nfae = NFAE(states, alphabet, transitions, start_state, accept_states)

# input_string = input("Enter a string ending with $:")
# # input_string = input_string.strip() + '$'
#
# if nfae.is_string_accepted(input_string):
#     print("YES")
# else:
#     print("NO")
def main():
    root = tk.Tk()
    app = NFAEBuilder(root)
    root.mainloop()


if __name__ == "__main__":
    main()
