
"""
The below code was created for Assignment 2 SystemsEngineering 5400
@author Brighid Meredith
Team 13
"""
class Architectures:
    def remove_duplicates(self,l):
        l = sorted([sorted(l[i]) for i in range(len(l))])
        rdl = [l[i] for i in range(len(l)) if l[i] != l[i-1] or i == 0]
        return rdl

    # This will return a list of all possible down-select architectures
    #  Required parameter: list of options
    def ds_arch(self,list_of_options):
        list_of_architectures = [list_of_options]
        for i in range(len(list_of_options)):
        # Remove item i from a copy of list and recursive call to ds_arch
            reduced_list_of_options = list_of_options[:i] + list_of_options[i+1:]
            if len(reduced_list_of_options) >= 0:
                list_of_architectures += self.ds_arch(reduced_list_of_options)
        return self.remove_duplicates(list_of_architectures)



    # This will return a list of all possible assignments
    # Required param: list of items being assigned, list of elements to assign  to
    # each item can be assigned to multiple elements or not assigned at  all
    def as_arch(self,M, N):
        # Get a list of all possible ways to assign each element
        possible_ways_to_assign = [(M[m], N[n]) for n in range(len(N)) for m in range(len(M))]
        # Given a list of possible assignments, calculate all possible
        return self.remove_duplicates(self.ds_arch(possible_ways_to_assign))

    # Return a list of all architectures
    # Required param: list of decisions, item to append to architecture
    # a recursive function
    def all_arch(self,decisions, arch):
        archs = [] # will list each architecture
        decision_options = decisions[0]
        decisions_remaining = decisions[1:]
        for d in decision_options:  # Cycle through each option for this decision
            temp_arch = arch + [d]  # Append option to temp arch
            if len(decisions_remaining) > 0:
                # Get list of subsequent architectures using this temp_arch
                temp_archs = self.all_arch(decisions_remaining, temp_arch)
                for ta in temp_archs:
                    archs.append(ta)
            else:  # No more subdecisions to iterate
                archs.append(temp_arch)
        return archs

